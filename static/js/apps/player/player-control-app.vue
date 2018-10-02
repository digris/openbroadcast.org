<script src="./player-control-app.js"></script>

<style lang="scss" scoped>
    @import '../../../sass/site/variables';
    .player-control-app {
        display: none;
        background: white;
        position: fixed;
        z-index: 99;
        bottom: 10px;
        left: 10px;
    }
</style>

<template>
    <div class="player-control-app player-control-container">
        <div class="debug-container">
            <button @click="player_play_all">PLAY ALL ON PAGE</button>
            <p>
                has master: {{ has_master }}
            </p>
            <ul>
                <li @click="player_load_from_api">player_load_from_api</li>
            </ul>
        </div>
    </div>
</template>
