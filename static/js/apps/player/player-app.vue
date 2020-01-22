<script src="./player-app.js"></script>

<style lang="scss" scoped>
  @import '../../../sass/site/variables';

  .player-app {
    background: white;
  }

  .player-container {
    display: flex;
    flex-direction: column;
    height: 100%;

    header {
      background: #fff;
    }

    main {
      flex: 1;
      overflow: auto;
    }

    footer {
      height: 32px;
    }
  }

  .player-current-item {
    min-height: 132px;

    .primary-content {
      display: flex;
      padding: 10px;

      .meta {
        flex-grow: 1;
      }

      .visual {
        img {
          width: 80px;
          height: 80px;
        }
      }
    }

    .plahead {
      height: 30px;

      img {
        width: 100%;
        height: 32px;
      }
    }
  }

  .player-current-item-loading {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 112px;

    color: white;
    font-weight: 300;
    font-size: 150%;

    background: $primary-color-b;
  }

  .player-controls {
    display: flex;
    align-items: center;
    justify-content: center;
    //border-top: 1px solid black;
    padding: 4px 0;

    .button-panel .fa {
      margin: 0 4px;

      color: #a5a5a5;
      font-size: 20px;
    }
  }

  .player-content {
    position: relative;
    //border-top: 1px solid black;
    //border-bottom: 1px solid black;
    flex-direction: column; /* stacks them vertically */
    height: 100%; /* needs to take the parents height, alternative: body {display: flex} */

    .item-to-play {
      margin: 0 0 10px;

      background: #fff;

      .header {
        padding: 2px 2px 2px 5px;

        background: #fff;
        border-top: 1px solid #eaeaea;
        border-bottom: 1px solid #eaeaea;
      }
    }
  }

  /*
    .player-footer {
        border-top: 1px solid #eaeaea;
        padding: 2px 2px 0 5px;
    }
    */

  .autoplay-container {
    position: fixed;
    top: 0;
    z-index: 99;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    width: 100%;
    height: 100%;

    background: $primary-color-b;

    .autoplay-panel {
      display: flex;

      /* flex-grow: 1; */

      /* flex-shrink: 1; */
      flex-basis: auto;
      flex-direction: row;
      align-items: center;
      justify-content: center;
      width: 240px;
      height: 240px;

      color: $primary-color-b;
      text-align: center;

      background: white;
      border-radius: 120px;
      cursor: pointer;
    }

    .autoplay-info {
      display: block;

      p {
        max-width: 320px;
        margin-top: 20px;
        padding: 0;

        color: white;
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

    background: rgba(255, 255, 255, 0.9);
  }

  .fade-enter-active {
    transition: all 0.05s;
  }

  .fade-leave-active {
    transition: all 0.3s;
  }

  .fade-enter,
  .fade-leave-to {
    opacity: 0;
  }

</style>

<template>
  <div class="player-app player-container">
    <div
      v-if="(!player)"
      class="player-overlay"
    >
      <div
        v-if="(!player)"
        class="initialising"
      >
        <p>Initialising player.<br>Please be patient.</p>
      </div>
    </div>

    <header>
      <div class="player-current-item">
        <div
          v-if="player_current_media"
          :key="player_current_media.content.uuid"
        >
          <div class="primary-content">
            <div class="meta">
              <a
                href="#"
                @click.prevent="visit(player_current_media.content)"
              >{{ player_current_media.content.name }}</a>
              <br>
              <a
                href="#"
                @click.prevent="visit(player_current_media.content, 'artist')"
              >{{ player_current_media.content.artist_display }}</a>
              <br>
              <a
                href="#"
                @click.prevent="visit(player_current_media.content, 'release')"
              >{{ player_current_media.content.release_display }}</a>
            </div>

            <div class="visual">
              <img :src="player_current_media.content.image">
            </div>
          </div>

          <div class="plahead">
            <waveform
              :key="player_current_media.uuid"
              :item="player_current_media"
              @seek="player_controls('seek', ...arguments)"
            />
          </div>
        </div>
        <div
          v-else
          class="player-current-item-loading"
        >
          loading...
        </div>
      </div>


      <div class="player-controls">
        <div class="button-panel">
          <a @click.prevent="player_play_offset(-1, player_current_media)">
            <i class="fa fa-step-backward" />
          </a>
          <!--
                    <a v-on:click.prevent="player_controls('stop')">
                        <i class="fa fa-stop"></i>
                    </a>
                    -->
          <a @click.prevent="player_controls('pause')">
            <i class="fa fa-pause" />
          </a>
          <a @click.prevent="player_controls('play')">
            <i class="fa fa-play" />
          </a>
          <a @click.prevent="player_play_offset(1, player_current_media)">
            <i class="fa fa-step-forward" />
          </a>
        </div>
      </div>
    </header>

    <main>
      <div class="player-content">
        <div
          v-if="(itemsToPlay && can_autoplay )"
          class="items-to-play"
        >
          <!-- eslint-disable-next-line vue/no-use-v-if-with-v-for -->
          <div
            v-for="item_to_play in itemsToPlay"
            :key="item_to_play.uuid"
          >
            <!--<div v-if="(item_to_play.items && item_to_play.items.length > 0)"></div>-->
            <transition name="fade">
              <div class="item-to-play">
                <div class="header">
                  <span class="name">{{ item_to_play.name }}<!-- {{ item_to_play.ct }}--></span>
                </div>

                <media
                  v-for="item in item_to_play.items"
                  :key="item.key"
                  :item="item"
                  @play="player_controls('play', ...arguments)"
                  @pause="player_controls('pause', ...arguments)"
                  @seek="player_controls('seek', ...arguments)"
                  @remove="player_controls('remove', ...arguments)"
                  @visit="visit(...arguments)"
                />
              </div>
            </transition>
          </div>
        </div>


        <transition name="fade">
          <div
            v-if="(! can_autoplay)"
            class="autoplay-container"
          >
            <div
              class="autoplay-panel"
              @click="player_resume_blocked_autoplay"
            >
              <span
                class="autoplay-button"
                @click="player_resume_blocked_autoplay"
              >
                Click to play
              </span>
            </div>

            <div class="autoplay-info">
              <p>
                Your browser prevents audio from automatically playing.<br>
                When opening the Open Broadcast player for the first time you have
                to manually start the playback.
              </p>
            </div>
          </div>
        </transition>

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
    </main>

    <footer>
      <playerfooter :items-to-play="itemsToPlay" />

      <!--
            <div class="player-footer">
                (( footer )) <span @click="add_all_to_playlist">Add all</span>
            </div>
            -->
    </footer>
  </div>
</template>
