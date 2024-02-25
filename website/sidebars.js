/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

 module.exports = {
  docsSidebar: [
    {
      type: 'category',
      label: 'Getting Started',
      items: [
        {
          type: 'doc',
          id: 'getting-started/introduction',
          label: 'Introduction',
        },
        {
          type: 'doc',
          id: 'getting-started/human-in-the-loop',
          label: 'Human in the Loop',
        },
        {
          type: 'doc',
          id: 'getting-started/code-executors',
          label: 'Code Executors',
        },
        {
          type: 'doc',
          id: 'getting-started/conversation-patterns',
          label: 'Conversation Patterns',
        },
        {
          type: 'doc',
          id: 'getting-started/what-is-next',
          label: 'What is Next?',
        }
      ],
    },
    {
      type: "category",
      label: "Installation",
      collapsed: true,
      items: ["installation/Docker", "installation/Optional-Dependencies"],
      link: {
        type: 'doc',
        id: "installation/Installation"
      },
    },
    {
      type: 'category',
      label: 'Topics',
      items: [
        'llm_configuration',
      ],
    },
    // {
    //   type: 'category',
    //   label: 'Advanced Topics',
    //   items: [
    //   ],
    // },
    {'Use Cases': [{type: 'autogenerated', dirName: 'Use-Cases'}]},
    'Contribute',
    'Research',
    'Migration-Guide'
  ],
  // pydoc-markdown auto-generated markdowns from docstrings
  referenceSideBar: [require("./docs/reference/sidebar.json")],
  notebooksSidebar: [
    {
      type: "category",
      label: "Notebooks",
      items: [{
        type: "autogenerated",
        dirName: "notebooks",
      },],
      link: {
        type: 'doc',
        id: "notebooks"
      },
    },

  ]
};
