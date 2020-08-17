<script src="./collector-app.js"></script>

<style lang="scss" scoped>
  @import '../../../sass/site/variables';

  // custom scroll-bar
  @mixin custom-scroll-bar() {
    &::-webkit-scrollbar {
      width: 4px;
      height: 10px;

      border-radius: 0;
    }

    &::-webkit-scrollbar-thumb {
      background: #fff;
      border-radius: 0;
    }

    &::-webkit-scrollbar-track {
      border-radius: 0;
    }
  }

  .collector-container {
    display: flex;
    flex-direction: column;
    height: 100%;

    .content-container {
      display: flex;
      flex: 1;
    }
  }

  .batch-collect {
    padding: 20px 6px;

    p {
      color: #fff;
    }
  }

  .item-to-collect {
    margin-top: 10px;
    margin-bottom: 10px;
    padding: 6px;

    color: #fff;

    .item {
      // background: rgba(#000, .9);
      display: flex;

      .visual {
        width: 52px;

        figure {
          margin: 0;
        }
      }

      .information {
        flex-grow: 1;
        padding: 2px 10px;
      }
    }
  }

  .settings-container {
    padding: 0 6px 6px 80px;

    .setting {
      display: flex;

      label {
        margin-top: 4px;
        padding-left: 10px;

        color: rgba(255, 255, 255, 0.7);
      }

      input {
        //position: relative;
      }
    }
  }

  .tabbed-navigation {
    display: flex;

    border-bottom: 1px solid $primary-color-b;

    .tab-selector {
      flex-grow: 1;
      margin: 0 6px;
      padding: 2px;

      color: #fff;
      text-align: center;
      text-transform: uppercase;

      cursor: pointer;

      &:not(:last-child) {
        margin-right: 1px;
      }

      &:hover {
        background: #000;
      }

      &.selected {
        background: $primary-color-b;
      }
    }
  }

  .playlist-search {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    height: 100%;

    .input-container {
      margin: 12px 0;
      padding: 6px;

      .input-group {
        .input-group-field {
          box-sizing: border-box;
          width: 100%;
          height: 26px;
          padding-left: 6px;

          color: #fff;

          background: transparent;
          border: 1px solid #444;
        }
      }
    }

    .list-container {
      @include custom-scroll-bar;

      flex: 1;
      max-height: 70vh;
      overflow: auto;
    }
  }

  .playlist-create {
    position: relative;

    width: 100%;

    .playlist-created-container {
      margin-top: 20px;
    }

    .input-container {
      margin: 12px 0;
      padding: 6px;

      .input-group {
        margin-bottom: 12px;

        .title {
          color: rgba(255, 255, 255, 0.7);
        }

        label {
          color: #fff;
        }

        .input-group-field {
          box-sizing: border-box;
          width: 100%;
          height: 26px;
          padding-left: 6px;

          color: #fff;

          background: transparent;
          border: 1px solid #444;
        }

        &.submit {
          padding: 20px 0 0 0;

          text-align: center;

          .button {
            padding: 6px 24px;

            color: $primary-color-b;
            text-transform: uppercase;

            background: #fff;
            border: 2px solid $primary-color-b;

            transition: border-radius 0.2s;

            &:hover {
              color: #fff;
              text-decoration: none;

              background: $primary-color-b;
              border-radius: 4px;
            }
          }
        }
      }

      .horizontal-radio-group {
        display: flex;
        align-items: center;
        justify-content: center;

        .title {
          margin-right: 20px;
        }

        label {
          display: flex;
          margin: 0 20px 0 0;

          color: rgba(255, 255, 255, 0.7);
        }

        input {
          margin-right: 6px;
        }
      }

      .form-errors {
        color: orangered;
        text-align: center;
      }
    }
  }

  .loading-container {
    position: absolute;
    top: 0;
    z-index: 99;

    display: flex;
    flex-direction: row;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;

    background: rgba(34, 34, 34, 1);
  }

  .fade-enter-active {
    transition: all 0.5s;
  }

  .fade-leave-active {
    transition: all 0.5s;
  }

  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }

</style>

<template>
  <modal
    :show="show_modal"
    :scope="scope"
    @close="show_modal=false"
  >
    <div
      slot="content"
      class="collector-app collector-container"
    >
      <header>
        <div
          v-if="(itemsToCollect && itemsToCollect.length > 1)"
          class="batch-collect"
        >
          <p>
            (( multiple)) {{ itemsToCollect.length }}
          </p>
        </div>
        <div
          v-for="item_to_collect in itemsToCollect"
          v-else
          :key="item_to_collect.uuid"
          class="item-to-collect"
        >
          <div class="item">
            <div class="visual">
              <visual :url="item_to_collect.content.image" />
            </div>
            <div class="information">
              {{ item_to_collect.content.name }}
              <br>
              {{ item_to_collect.content.artist_display }}
              |
              {{ item_to_collect.content.release_display }}
              <br>
              {{ item_to_collect.duration | msToTime }}
            </div>
          </div>
        </div>
        <div class="tabbed-navigation">
          <div
            :class="{ selected: (scope === 'list') }"
            class="tab-selector"
            @click.prevent="set_scope_list"
          >
            <span>Your Playlists</span>
          </div>
          <div
            :class="{ selected: (scope === 'create') }"
            class="tab-selector"
            @click.prevent="set_scope_create"
          >
            <span>New Playlist</span>
          </div>
        </div>
      </header>

      <div class="content-container">
        <div
          v-if="(scope === 'list')"
          class="playlist-search"
        >
          <div class="input-container">
            <div class="input-group">
              <input
                class="input-group-field"
                type="text"
                placeholder="Search playlists"
                :value="query_string"
                @input="update_query_string"
              >
            </div>
          </div>
          <div
            v-if="playlists"
            class="list-container scrollable"
          >
            <playlist
              v-for="item in playlists"
              :key="item.uuid"
              :item="item"
              :items-to-collect="itemsToCollect"
              :actions="['add', 'add-and-close']"
              @visit="visit(...arguments)"
              @add="add_item_to_playlist(...arguments)"
            />
          </div>
        </div>

        <div
          v-if="(scope === 'create')"
          class="playlist-create"
        >
          <transition name="fade">
            <div
              v-if="create_playlist_data.created"
              class="playlist-created-container"
            >
              <playlist
                :key="create_playlist_data.created.uuid"
                :item="create_playlist_data.created"
                :items-to-collect="itemsToCollect"
                :actions="['visit']"
                @visit="visit(...arguments)"
              />
            </div>
          </transition>

          <form
            v-if="(! create_playlist_data.created)"
            @submit.prevent="create_playlist"
          >
            <div class="input-container">
              <div class="input-group">
                <label for="playlist_create_name">Playlist title *</label>
                <input
                  id="playlist_create_name"
                  ref="playlist_create_name"
                  v-model="create_playlist_data.name"
                  class="input-group-field"
                  type="text"
                  autofocus
                  autocomplete="off"
                >
              </div>
              <div class="input-group">
                <div class="horizontal-radio-group">
                  <span class="title">Playlist will be</span>
                  <label>
                    <input
                      v-model="create_playlist_data.type"
                      type="radio"
                      name="type"
                      value="basket"
                    >private
                  </label>

                  <label>
                    <input
                      v-model="create_playlist_data.type"
                      type="radio"
                      name="type"
                      value="playlist"
                    >public
                  </label>
                </div>
              </div>

              <div
                v-if="create_playlist_data.errors.length"
                class="form-errors"
              >
                <span>Please correct the following error(s):</span>
                <ul>
                  <li
                    v-for="error in create_playlist_data.errors"
                    :key="error"
                  >
                    {{ error }}
                  </li>
                </ul>
              </div>

              <div class="input-group submit">
                <input
                  type="submit"
                  value="Save"
                  class="button"
                >
              </div>
            </div>
          </form>

          <transition name="fade">
            <div
              v-if="loading"
              class="loading-container"
            >
              <span class="loading-info">
                <loader />
              </span>
            </div>
          </transition>
        </div>
      </div>
    </div>
  </modal>
</template>
