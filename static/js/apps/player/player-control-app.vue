<script src="./player-control-app.js"></script>

<style lang="scss" scoped>
    @import '../../../sass/site/variables';
    .player-control-app {
        display: block;
        background: white;
        position: fixed;
        z-index: 99;
        bottom: 10px;
        left: 10px;
    }
</style>

<template>
    <div v-if="enabled" class="player-control-app player-control-container">
        <div class="debug-container">
            <button @click="player_play_all">PLAY ALL ON PAGE</button>
            <p>
                has master: {{ has_master }}
            </p>
        </div>
    </div>
</template>
