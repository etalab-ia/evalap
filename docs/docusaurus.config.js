// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const { themes } = require('prism-react-renderer');


/** @type {import('@docusaurus/types').Config} */
const config = {
    title: 'Evalap',
    tagline: 'Evaluation API and Platform for LLM models',
    favicon: 'img/favicon.ico',

    // Set the production url of your site here
    url: 'https://evalap.etalab.gouv.fr',
    // Set the /<baseUrl>/ pathname under which your site is served
    // For GitHub pages deployment, it is often '/<projectName>/'
    baseUrl: '/doc/',

    // GitHub pages deployment config.
    // If you aren't using GitHub pages, you don't need these.
    organizationName: 'etalab-ia', // Usually your GitHub org/user name.
    projectName: 'evalap', // Usually your repo name.
    deploymentBranch: 'main',
    trailingSlash: false,

    onBrokenLinks: 'throw',
    onBrokenMarkdownLinks: 'warn',

    // Even if you don't use internalization, you can use this field to set useful
    // metadata like html lang. For example, if your site is Chinese, you may want
    // to replace "en" with "zh-Hans".
    i18n: {
        defaultLocale: 'en',
        locales: ['en', 'fr'],
    },

    presets: [
        [
            'classic',
            /** @type {import('@docusaurus/preset-classic').Options} */
            ({
                docs: {
                    sidebarPath: require.resolve('./sidebars.js'),
                    // Please change this to your repo.
                    // Remove this to remove the "edit this page" links.
                    editUrl: 'https://github.com/etalab-ia/evalap/tree/main/docs/',
                    sidebarCollapsed: false,
                },
                blog: false,
                theme: {
                    customCss: require.resolve('./src/css/custom.css'),
                },
            }),
        ],
    ],

    themeConfig:
        /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
        ({
            metadata: [
                { name: "algolia-site-verification", content: "766474FDFEC7E852" },
            ],
            // Replace with your project's social card
            image: 'img/android-chrome-512x512.png',
            navbar: {
                title: 'EvalAP',
                hideOnScroll: true,
                logo: {
                    alt: 'EvalAP Logo',
                    src: 'img/favicon.ico',
                    href: '/',
                },
                items: [
                    {
                        type: 'docSidebar',
                        sidebarId: 'tutorialSidebar',
                        label: 'Documentation',
                        position: 'left',
                    },
                    {
                        label: 'API Reference',
                        href: "https://evalap.etalab.gouv.fr/redoc",
                        position: 'left',
                    },
                    {
                        type: 'search',
                        position: 'right',
                    },
                    {
                        label: 'Github',
                        href: 'https://github.com/etalab-ia/evalap',
                        position: 'right',
                    },
                    {
                        type: 'localeDropdown',
                        position: 'right',
                    },
                ],
            },
            footer: {
                style: 'dark',
                links: [
                    {
                        title: 'Docs',
                        items: [
                            {
                                label: 'Getting Started',
                                to: '/docs/getting-started/install-with-docker',
                            },
                            {
                                label: 'User Guides',
                                to: '/docs/user-guides/add-your-dataset',
                            },
                            {
                                label: 'Developer Guide',
                                to: '/docs/developer-guide/adding-a-new-metric',
                            },
                        ],
                    },
                    {
                        title: 'Community',
                        items: [
                            {
                                label: 'GitHub Issues',
                                href: 'https://github.com/etalab-ia/evalap/issues',
                            },
                            {
                                label: 'Discussions',
                                href: 'https://github.com/etalab-ia/evalap/discussions',
                            },
                        ],
                    },
                    {
                        title: 'More',
                        items: [
                            {
                                label: 'Official instance',
                                href: 'https://evalap.etalab.gouv.fr',
                            },
                            {
                                label: 'API Reference',
                                href: 'https://evalap.etalab.gouv.fr/redoc',
                            },
                            {
                                label: 'API Swagger',
                                href: 'https://evalap.etalab.gouv.fr/docs',
                            },
                            {
                                label: 'Github',
                                href: 'https://github.com/etalab-ia/evalap',
                            },
                        ],
                    },
                ],
                copyright: `Copyright © ${new Date().getFullYear()} Etalab.`,
            },
            algolia: {
                // The application ID provided by Algolia
                appId: 'L16S9RBKXB',

                // Public API key: it is safe to commit it
                apiKey: 'beb495bea76be681f1a65d23a0afcb17',

                indexName: 'EvalAP 2',
            },
            prism: {
                theme: themes.github,
                darkTheme: themes.dracula,
            },
        }),
};

module.exports = config;
