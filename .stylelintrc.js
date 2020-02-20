module.exports = {
  "extends": [
    "stylelint-scss",
    "stylelint-config-rational-order"
  ],
  "rules": {
    "indentation": 2,
    "at-rule-no-unknown": null,
    "no-descending-specificity": null,
    "order/properties-order": [],
    "plugin/rational-order": [
      true,
      {
        "border-in-box-model": false,
        "empty-line-between-groups": true
      }
    ]
  }
}
