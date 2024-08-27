#!/usr/bin/env python3 -m pytest

import os
import shutil
import sys
import time

import pytest

from autogen import OpenAIWrapper, config_list_from_json
from autogen.cache.cache import Cache
from autogen.oai.client import LEGACY_CACHE_DIR, LEGACY_DEFAULT_CACHE_SEED

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from conftest import skip_openai  # noqa: E402

TOOL_ENABLED = False
try:
    import openai
    from openai import OpenAI

    if openai.__version__ >= "1.1.0":
        TOOL_ENABLED = True
    from openai.types.chat.chat_completion import ChatCompletionMessage
except ImportError:
    skip = True
else:
    skip = False or skip_openai

KEY_LOC = "notebook"
OAI_CONFIG_LIST = "OAI_CONFIG_LIST"


@pytest.mark.skipif(skip, reason="openai>=1 not installed")
def test_aoai_chat_completion():
    config_list = config_list_from_json(
        env_or_file=OAI_CONFIG_LIST,
        file_location=KEY_LOC,
        filter_dict={"api_type": ["azure"], "tags": ["gpt-3.5-turbo"]},
    )
    client = OpenAIWrapper(config_list=config_list)
    response = client.create(messages=[{"role": "user", "content": "2+2="}], cache_seed=None)
    print(response)
    print(client.extract_text_or_completion_object(response))

    # test dialect
    config = config_list[0]
    config["azure_deployment"] = config["model"]
    config["azure_endpoint"] = config.pop("base_url")
    client = OpenAIWrapper(**config)
    response = client.create(messages=[{"role": "user", "content": "2+2="}], cache_seed=None)
    print(response)
    print(client.extract_text_or_completion_object(response))


@pytest.mark.skipif(skip or not TOOL_ENABLED, reason="openai>=1.1.0 not installed")
def test_oai_tool_calling_extraction():
    config_list = config_list_from_json(
        env_or_file=OAI_CONFIG_LIST,
        file_location=KEY_LOC,
        filter_dict={"api_type": ["azure"], "tags": ["gpt-3.5-turbo"]},
    )
    client = OpenAIWrapper(config_list=config_list)
    response = client.create(
        messages=[
            {
                "role": "user",
                "content": "What is the weather in San Francisco?",
            },
        ],
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "getCurrentWeather",
                    "description": "Get the weather in location",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
                            "unit": {"type": "string", "enum": ["c", "f"]},
                        },
                        "required": ["location"],
                    },
                },
            }
        ],
    )
    print(response)
    print(client.extract_text_or_completion_object(response))


@pytest.mark.skipif(skip, reason="openai>=1 not installed")
def test_chat_completion():
    config_list = config_list_from_json(
        env_or_file=OAI_CONFIG_LIST,
        file_location=KEY_LOC,
    )
    client = OpenAIWrapper(config_list=config_list)
    response = client.create(messages=[{"role": "user", "content": "1+1="}])
    print(response)
    print(client.extract_text_or_completion_object(response))


@pytest.mark.skipif(skip, reason="openai>=1 not installed")
def test_completion():
    config_list = config_list_from_json(
        env_or_file=OAI_CONFIG_LIST,
        file_location=KEY_LOC,
        filter_dict={"tags": ["gpt-35-turbo-instruct", "gpt-3.5-turbo-instruct"]},
    )
    client = OpenAIWrapper(config_list=config_list)
    response = client.create(prompt="1+1=")
    print(response)
    print(client.extract_text_or_completion_object(response))


@pytest.mark.skipif(skip, reason="openai>=1 not installed")
@pytest.mark.parametrize(
    "cache_seed",
    [
        None,
        42,
    ],
)
def test_cost(cache_seed):
    config_list = config_list_from_json(
        env_or_file=OAI_CONFIG_LIST,
        file_location=KEY_LOC,
        filter_dict={"tags": ["gpt-35-turbo-instruct", "gpt-3.5-turbo-instruct"]},
    )
    client = OpenAIWrapper(config_list=config_list, cache_seed=cache_seed)
    response = client.create(prompt="1+3=")
    print(response.cost)


@pytest.mark.skipif(skip, reason="openai>=1 not installed")
def test_customized_cost():
    config_list = config_list_from_json(
        env_or_file=OAI_CONFIG_LIST, file_location=KEY_LOC, filter_dict={"tags": ["gpt-3.5-turbo-instruct"]}
    )
    for config in config_list:
        config.update({"price": [1000, 1000]})
    client = OpenAIWrapper(config_list=config_list, cache_seed=None)
    response = client.create(prompt="1+3=")
    assert (
        response.cost >= 4
    ), f"Due to customized pricing, cost should be > 4. Message: {response.choices[0].message.content}"


@pytest.mark.skipif(skip, reason="openai>=1 not installed")
def test_usage_summary():
    config_list = config_list_from_json(
        env_or_file=OAI_CONFIG_LIST,
        file_location=KEY_LOC,
        filter_dict={"tags": ["gpt-35-turbo-instruct", "gpt-3.5-turbo-instruct"]},
    )
    client = OpenAIWrapper(config_list=config_list)
    response = client.create(prompt="1+3=", cache_seed=None)

    # usage should be recorded
    assert client.actual_usage_summary["total_cost"] > 0, "total_cost should be greater than 0"
    assert client.total_usage_summary["total_cost"] > 0, "total_cost should be greater than 0"

    # check print
    client.print_usage_summary()

    # check clear
    client.clear_usage_summary()
    assert client.actual_usage_summary is None, "actual_usage_summary should be None"
    assert client.total_usage_summary is None, "total_usage_summary should be None"

    # actual usage and all usage should be different
    response = client.create(prompt="1+3=", cache_seed=42)
    assert client.total_usage_summary["total_cost"] > 0, "total_cost should be greater than 0"
    client.clear_usage_summary()
    response = client.create(prompt="1+3=", cache_seed=42)
    assert client.actual_usage_summary is None, "No actual cost should be recorded"

    # check update
    response = client.create(prompt="1+3=", cache_seed=42)
    assert (
        client.total_usage_summary["total_cost"] == response.cost * 2
    ), "total_cost should be equal to response.cost * 2"


@pytest.mark.skipif(skip, reason="openai>=1 not installed")
def test_legacy_cache():
    config_list = config_list_from_json(
        env_or_file=OAI_CONFIG_LIST,
        file_location=KEY_LOC,
        filter_dict={"tags": ["gpt-3.5-turbo"]},
    )

    # Prompt to use for testing.
    prompt = "Write a 100 word summary on the topic of the history of human civilization."

    # Clear cache.
    if os.path.exists(LEGACY_CACHE_DIR):
        shutil.rmtree(LEGACY_CACHE_DIR)

    # Test default cache seed.
    client = OpenAIWrapper(config_list=config_list)
    start_time = time.time()
    cold_cache_response = client.create(messages=[{"role": "user", "content": prompt}])
    end_time = time.time()
    duration_with_cold_cache = end_time - start_time

    start_time = time.time()
    warm_cache_response = client.create(messages=[{"role": "user", "content": prompt}])
    end_time = time.time()
    duration_with_warm_cache = end_time - start_time
    assert cold_cache_response == warm_cache_response
    assert duration_with_warm_cache < duration_with_cold_cache
    assert os.path.exists(os.path.join(LEGACY_CACHE_DIR, str(LEGACY_DEFAULT_CACHE_SEED)))

    # Test with cache seed set through constructor
    client = OpenAIWrapper(config_list=config_list, cache_seed=13)
    start_time = time.time()
    cold_cache_response = client.create(messages=[{"role": "user", "content": prompt}])
    end_time = time.time()
    duration_with_cold_cache = end_time - start_time

    start_time = time.time()
    warm_cache_response = client.create(messages=[{"role": "user", "content": prompt}])
    end_time = time.time()
    duration_with_warm_cache = end_time - start_time
    assert cold_cache_response == warm_cache_response
    assert duration_with_warm_cache < duration_with_cold_cache
    assert os.path.exists(os.path.join(LEGACY_CACHE_DIR, str(13)))

    # Test with cache seed set through create method
    client = OpenAIWrapper(config_list=config_list)
    start_time = time.time()
    cold_cache_response = client.create(messages=[{"role": "user", "content": prompt}], cache_seed=17)
    end_time = time.time()
    duration_with_cold_cache = end_time - start_time

    start_time = time.time()
    warm_cache_response = client.create(messages=[{"role": "user", "content": prompt}], cache_seed=17)
    end_time = time.time()
    duration_with_warm_cache = end_time - start_time
    assert cold_cache_response == warm_cache_response
    assert duration_with_warm_cache < duration_with_cold_cache
    assert os.path.exists(os.path.join(LEGACY_CACHE_DIR, str(17)))

    # Test using a different cache seed through create method.
    start_time = time.time()
    cold_cache_response = client.create(messages=[{"role": "user", "content": prompt}], cache_seed=21)
    end_time = time.time()
    duration_with_cold_cache = end_time - start_time
    assert duration_with_warm_cache < duration_with_cold_cache
    assert os.path.exists(os.path.join(LEGACY_CACHE_DIR, str(21)))


@pytest.mark.skipif(skip, reason="openai>=1 not installed")
def test_cache():
    config_list = config_list_from_json(
        env_or_file=OAI_CONFIG_LIST,
        file_location=KEY_LOC,
        filter_dict={"tags": ["gpt-3.5-turbo"]},
    )

    # Prompt to use for testing.
    prompt = "Write a 100 word summary on the topic of the history of artificial intelligence."

    # Clear cache.
    if os.path.exists(LEGACY_CACHE_DIR):
        shutil.rmtree(LEGACY_CACHE_DIR)
    cache_dir = ".cache_test"
    assert cache_dir != LEGACY_CACHE_DIR
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    # Test cache set through constructor.
    with Cache.disk(cache_seed=49, cache_path_root=cache_dir) as cache:
        client = OpenAIWrapper(config_list=config_list, cache=cache)
        start_time = time.time()
        cold_cache_response = client.create(messages=[{"role": "user", "content": prompt}])
        end_time = time.time()
        duration_with_cold_cache = end_time - start_time

        start_time = time.time()
        warm_cache_response = client.create(messages=[{"role": "user", "content": prompt}])
        end_time = time.time()
        duration_with_warm_cache = end_time - start_time
        assert cold_cache_response == warm_cache_response
        assert duration_with_warm_cache < duration_with_cold_cache
        assert os.path.exists(os.path.join(cache_dir, str(49)))
        # Test legacy cache is not used.
        assert not os.path.exists(os.path.join(LEGACY_CACHE_DIR, str(49)))
        assert not os.path.exists(os.path.join(cache_dir, str(LEGACY_DEFAULT_CACHE_SEED)))

    # Test cache set through method.
    client = OpenAIWrapper(config_list=config_list)
    with Cache.disk(cache_seed=312, cache_path_root=cache_dir) as cache:
        start_time = time.time()
        cold_cache_response = client.create(messages=[{"role": "user", "content": prompt}], cache=cache)
        end_time = time.time()
        duration_with_cold_cache = end_time - start_time

        start_time = time.time()
        warm_cache_response = client.create(messages=[{"role": "user", "content": prompt}], cache=cache)
        end_time = time.time()
        duration_with_warm_cache = end_time - start_time
        assert cold_cache_response == warm_cache_response
        assert duration_with_warm_cache < duration_with_cold_cache
        assert os.path.exists(os.path.join(cache_dir, str(312)))
        # Test legacy cache is not used.
        assert not os.path.exists(os.path.join(LEGACY_CACHE_DIR, str(312)))
        assert not os.path.exists(os.path.join(cache_dir, str(LEGACY_DEFAULT_CACHE_SEED)))

    # Test different cache seed.
    with Cache.disk(cache_seed=123, cache_path_root=cache_dir) as cache:
        start_time = time.time()
        cold_cache_response = client.create(messages=[{"role": "user", "content": prompt}], cache=cache)
        end_time = time.time()
        duration_with_cold_cache = end_time - start_time
        assert duration_with_warm_cache < duration_with_cold_cache
        # Test legacy cache is not used.
        assert not os.path.exists(os.path.join(LEGACY_CACHE_DIR, str(123)))
        assert not os.path.exists(os.path.join(cache_dir, str(LEGACY_DEFAULT_CACHE_SEED)))


@pytest.mark.skipif(skip, reason="openai>=1 not installed")
def test_chat_completion_after_tool_call():
    config_list = config_list_from_json(
        env_or_file=OAI_CONFIG_LIST,
        file_location=KEY_LOC,
        filter_dict={"tags": ["gpt-4o-mini"]},
    )
    client = OpenAIWrapper(config_list=config_list)
    params = {
        "messages": [
            {
                "content": "You are a student writing a practice test. Your "
                "task is as follows:\n"
                "  1) Retrieve exam questions by calling a "
                "function.\n"
                "  2) Write a draft of proposed answers and engage "
                "in dialogue with your tutor.\n"
                "  3) Once you are done with the dialogue, register "
                "the final answers by calling a function.\n"
                "  4) Retrieve the final grade by calling a "
                "function.\n"
                "Finally, terminate the chat by saying 'TERMINATE'.",
                "role": "system",
            },
            {"content": "Prepare for the test about Leonardo da Vinci.", "name": "Teacher_Agent", "role": "user"},
            {
                "content": None,
                "role": "assistant",
                "tool_calls": [
                    {
                        "function": {
                            "arguments": '{"message":"Please '
                            "provide the exam "
                            "questions for the "
                            "test about Leonardo "
                            'da Vinci."}',
                            "name": "retrieve_exam_questions",
                        },
                        "id": "call_WtPX2rq3saIIqk4hM4jjAhNY",
                        "type": "function",
                    }
                ],
            },
            {
                "content": "1) Mona Lisa 2) Innovations 3) Florence at the time "
                "of Leonardo 4) The Last Supper 5) Vit",
                "role": "tool",
                "tool_call_id": "call_WtPX2rq3saIIqk4hM4jjAhNY",
            },
            {
                "content": "I have retrieved the exam questions about Leonardo "
                "da Vinci. Here they are:\n"
                "\n"
                "1. Mona Lisa\n"
                "2. Innovations\n"
                "3. Florence at the time of Leonardo\n"
                "4. The Last Supper\n"
                "5. Vitruvian Man\n"
                "\n"
                "Now, I'll draft proposed answers for each question. "
                "Let's start with the first one: \n"
                "\n"
                "1. **Mona Lisa**: The Mona Lisa, painted by "
                "Leonardo da Vinci in the early 16th century, is "
                "arguably the most famous painting in the world. It "
                "is known for the subject's enigmatic expression and "
                "da Vinci's masterful use of sfumato, which creates "
                "a soft transition between colors and tones.\n"
                "\n"
                "What do you think of this draft answer? Would you "
                "like to add or change anything?",
                "name": "Student_Agent",
                "role": "assistant",
            },
            {
                "content": "Your draft answer for the Mona Lisa is "
                "well-articulated and captures the essence of the "
                "painting and its significance. Here are a few "
                "suggestions to enhance your response:\n"
                "\n"
                "1. **Historical Context**: You could mention that "
                "the painting was created between 1503 and 1506 and "
                "is housed in the Louvre Museum in Paris.\n"
                "   \n"
                "2. **Artistic Techniques**: You might want to "
                "elaborate on the technique of sfumato, explaining "
                "how it contributes to the depth and realism of the "
                "portrait.\n"
                "\n"
                "3. **Cultural Impact**: It could be beneficial to "
                "touch on the painting's influence on art and "
                "culture, as well as its status as a symbol of the "
                "Renaissance.\n"
                "\n"
                "Here's a revised version incorporating these "
                "points:\n"
                "\n"
                "**Revised Answer**: The Mona Lisa, painted by "
                "Leonardo da Vinci between 1503 and 1506, is "
                "arguably the most famous painting in the world and "
                "is housed in the Louvre Museum in Paris. It is "
                "renowned for the subject's enigmatic expression, "
                "which has intrigued viewers for centuries. Da "
                "Vinci's masterful use of sfumato, a technique that "
                "allows for a soft transition between colors and "
                "tones, adds a remarkable depth and realism to the "
                "piece. The Mona Lisa has not only influenced "
                "countless artists and movements but has also become "
                "a symbol of the Renaissance and a cultural icon in "
                "its own right.\n"
                "\n"
                "Let me know if you would like to move on to the "
                "next question or make further adjustments!",
                "name": "Teacher_Agent",
                "role": "user",
            },
        ],
        "model": "gpt-4o-mini",
        "stream": False,
        "temperature": 0.8,
        "tools": [
            {
                "function": {
                    "description": "Get exam questions from examiner",
                    "name": "retrieve_exam_questions",
                    "parameters": {
                        "additionalProperties": False,
                        "properties": {"message": {"description": "Message " "for " "examiner", "type": "string"}},
                        "required": ["message"],
                        "type": "object",
                    },
                },
                "type": "function",
            },
            {
                "function": {
                    "description": "Write a final answers to exam "
                    "questions to examiner, but only after "
                    "discussing with the tutor first.",
                    "name": "write_final_answers",
                    "parameters": {
                        "additionalProperties": False,
                        "properties": {"message": {"description": "Message " "for " "examiner", "type": "string"}},
                        "required": ["message"],
                        "type": "object",
                    },
                },
                "type": "function",
            },
            {
                "function": {
                    "description": "Get the final grade after submitting " "the answers.",
                    "name": "get_final_grade",
                    "parameters": {
                        "additionalProperties": False,
                        "properties": {"message": {"description": "Message " "for " "examiner", "type": "string"}},
                        "required": ["message"],
                        "type": "object",
                    },
                },
                "type": "function",
            },
        ],
    }

    response = client.create(**params)

    assert response is not None


if __name__ == "__main__":
    # test_aoai_chat_completion()
    # test_oai_tool_calling_extraction()
    # test_chat_completion()
    test_completion()
    # # test_cost()
    # test_usage_summary()
    # test_legacy_cache()
    # test_cache()
