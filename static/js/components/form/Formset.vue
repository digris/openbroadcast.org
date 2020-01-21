<script>

    const DEBUG = true;

    export default {
        name: 'Formset',
        props: {
            id: {
                type: String,
                required: false,
            },
            autogrow: {
                type: Boolean,
                required: false,
                default: false,
            },
        },
        data: function () {
            return {
                autogrowNumRowsVisible: 1
            }
        },
        mounted: function () {
            if (this.autogrow) {
                if (DEBUG) {
                    console.debug('Formset - enable autogrow');
                }
                // bind input blur
                const inputs = this.$el.querySelectorAll("input");
                inputs.forEach((input, i) => {
                   input.addEventListener("blur", (e) => {
                       this.updateAutogrow();
                   });
                });
                // initial update
                this.updateAutogrow();
            }
        },
        methods: {
            updateAutogrow: function () {

                const rows = Array.from(
                    this.$el.querySelectorAll("[data-autogrow='autogrow']")
                );

                // get last row with data filled in
                rows.forEach((row, i) => {
                    const combinedInputLength = Array.from(
                        row.querySelectorAll(
                            "input:not([type=checkbox])"
                        )).reduce((acc, el) => acc + el.value.length, 0
                    );

                    if(combinedInputLength > 0) {
                        this.autogrowNumRowsVisible = i + 2;
                        return;
                    }
                });

                // update visibility
                rows.forEach((row, i) => {
                    if(i < this.autogrowNumRowsVisible) {
                        row.classList.remove('autogrow--hidden');
                    } else {
                        row.classList.add('autogrow--hidden');
                    }
                });
            }
        },
        computed: {},
    }

</script>
<style lang="scss" scoped>
    .formset {
        .form-grid-container {
            grid-template-columns: auto auto 100px;
        }

        .form-grid-cell {
            .input-container {
                grid-template-columns: 60px auto;
                margin: 0;
            }
        }

        // autogrow
        [data-autogrow] {
            transition: display 200ms;
            &.autogrow--hidden {
                display: none;
            }
        }
    }
</style>
<template>
    <div
        :class="{'autogrow': autogrow}"
        class="formset">
        <slot></slot>
    </div>
</template>
