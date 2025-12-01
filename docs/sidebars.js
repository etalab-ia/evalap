/**
 * Creating a sidebar enables you to:
 - create an ordered group of docs
 - render a sidebar for each doc of that group
 - provide next/previous navigation

 The sidebars can be generated from the filesystem, or explicitly defined here.

 Create as many sidebars as you want.
 */

// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
    // By default, Docusaurus generates a sidebar from the docs folder structure
    tutorialSidebar: [
        {
            type: 'doc',
            id: 'intro',
        },
        {
            type: 'category',
            label: 'Getting Started',
            items: [
                'getting-started/install-with-docker',
                'getting-started/install-from-source',
            ],
        },
        {
            type: 'category',
            label: 'User Guides',
            items: [
                'user-guides/add-your-dataset',
                'user-guides/create-a-simple-experiment',
                'user-guides/create-experiment-set',
                'user-guides/use-custom-llm-judge-prompt',
                'user-guides/run-answers-locally',
                'user-guides/evaluate-your-own-ia-system',
                'user-guides/create-compliance-experiment',
            ],
        },
        {
            type: 'category',
            label: 'Developer Guide',
            items: [
                'developer-guide/adding-a-new-metric',
                'developer-guide/increase-parallel-requests',
            ],
        },
    ],
};

module.exports = sidebars;
