<script>
    export default {
        name: 'TagInputAutocomplete',

        props: {
            items: {
                type: Array,
                required: false,
                default: () => [],
            },
            isAsync: {
                type: Boolean,
                required: false,
                default: false,
            },
        },

        data() {
            return {
                isOpen: false,
                results: [],
                search: '',
                isLoading: false,
                arrowCounter: 0,
            };
        },

        methods: {
            onChange() {
                // Let's warn the parent that a change was made
                this.$emit('input', this.search);

                // Is the data given by an outside ajax request?
                if (this.isAsync) {
                    if (this.items.length < 1) {
                        this.isLoading = true;
                    }
                } else {
                    // Let's  our flat array
                    this.filterResults();
                    this.isOpen = true;
                }
            },

            filterResults() {
                // first uncapitalize all the things
                this.results = this.items.filter((item) => {
                    return item.toLowerCase().indexOf(this.search.toLowerCase()) > -1;
                });
            },

            setResult(result) {
                this.arrowCounter = -1;
                this.isOpen = false;
                this.$emit('result', result);
                this.search = "";
            },
            onArrowDown(evt) {
                if (this.arrowCounter < this.results.length) {
                    this.arrowCounter = this.arrowCounter + 1;
                }
            },
            onArrowUp() {
                if (this.arrowCounter > 0) {
                    this.arrowCounter = this.arrowCounter - 1;
                }
            },
            onEnter() {

                // no result from autocomplete
                if (this.arrowCounter < 0) {
                    this.setResult(this.search);
                } else {
                    this.setResult(this.results[this.arrowCounter])
                }
            },
            handleClickOutside(evt) {
                if (!this.$el.contains(evt.target)) {
                    this.isOpen = false;
                    this.arrowCounter = -1;
                }
            }
        },
        watch: {
            items: function (val, oldValue) {

                // actually compare them
                if (val !== oldValue) {
                    this.results = val;
                    this.isLoading = false;
                    this.isOpen = true;
                }
            },
        },
        mounted() {
            document.addEventListener('click', this.handleClickOutside)
        },
        destroyed() {
            document.removeEventListener('click', this.handleClickOutside)
        }
    };
</script>

<template>
    <div class="autocomplete">
        <input
            type="text"
            maxlength="50"
            placeholder="Add Tag"
            @input="onChange"
            v-model="search"
            @keydown.down.prevent="onArrowDown"
            @keydown.up.prevent="onArrowUp"
            @keydown.enter.prevent="onEnter"
            @keydown.188.prevent="onEnter"
        />
        <ul
            v-show="isOpen"
            class="autocomplete__results"
        >
            <li
                class="loading"
                v-if="isLoading"
            >
                Loading tags...
            </li>
            <li
                v-else
                v-for="(result, i) in results"
                :key="i"
                @click="setResult(result)"
                class="autocomplete__result"
                :class="{ 'is-active': i === arrowCounter }"
            >
                {{ result }}
            </li>
        </ul>
    </div>
</template>

<style lang="scss" scoped>
    .autocomplete {
        position: relative;
        display: inline-block;
        width: 100%;

        input {
            height: 22px;
            line-height: 22px;
            padding: 0 .5rem;
            width: 100%;
        }

        &__results {
            padding: 0;
            margin: 0;
            // border: 1px solid #eeeeee;
            overflow: auto;
            min-width: 100%;
            min-height: 40px;
            position: absolute;
            background: white;
            z-index: 10;
            border: 1px solid #ededed;
            // border-top: 0;
            box-shadow: 1px 2px 3px 1px rgba(#000, .2);
        }

        &__result {
            list-style: none;
            text-align: left;
            padding: .5rem;
            cursor: pointer;

            &.is-active,
            &:hover {
                background: #e2d7f9;
            }
        }

    }

</style>
