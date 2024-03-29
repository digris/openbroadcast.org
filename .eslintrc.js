module.exports = {
  root: true,
  env: {
    node: true,
  },
  extends: [
    'plugin:vue/recommended',
    'airbnb-base',
    // '@vue/airbnb',
  ],
  // parser: "babel-eslint",
  rules: {
    // camelcase: [2, { properties: 'always' }],
    'camelcase': 'off',
    'no-undef': 'off',
    'no-console': 'off',
    'no-param-reassign': 'off',
    'import/prefer-default-export': 'off',
    'import/no-unresolved': 'off', // TODO: figure out how to handle webpack `alias` in eslint.
    // 'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    // https://github.com/babel/babel-eslint/issues/815#issuecomment-580670577
    "template-curly-spacing" : "off",
    "indent" : "off",
  },
  // overrides: [
  //   {
  //     files: ["*.vue"],
  //     rules: {
  //       'max-len': 120,
  //     },
  //   },
  // ],
  parserOptions: {
    "parser": "babel-eslint",
    "sourceType": "module"
  },
  plugins: [
    "vue",
  ],
};
