<script src="./player-app.js"></script>

<template>

    <div class="player-app player-container" v-bind:class="{ 'is-master': is_master, 'is-slave': is_slave }">
        <h1>PLAYER</h1>


        <div class="initialising" v-if="(!player)">
            <p>Initialising player.<br>Please be patient.</p>
        </div>

        <div class="controls">
            <div class="button-panel">
                <a v-on:click.prevent="player_controls('back')">
                    <i class="fa fa-step-backward"></i>
                </a>
                <a v-on:click.prevent="player_controls('stop')">
                    <i class="fa fa-stop"></i>
                </a>
                <a v-on:click.prevent="player_controls('pause')">
                    <i class="fa fa-pause"></i>
                </a>
                <a v-on:click.prevent="player_controls('play')">
                    <i class="fa fa-play"></i>
                </a>
                <a v-on:click.prevent="player_controls('forward')">
                    <i class="fa fa-step-forward"></i>
                </a>
            </div>
        </div>


        <div v-if="items_to_play" class="items-to-play">

            <item-container
                v-for="item_to_play in items_to_play"
                v-bind:key="item_to_play.uuid"
                v-bind:item_to_play="item_to_play"
                @play="player_controls('play', ...arguments)"
                @pause="player_controls('pause', ...arguments)"
                @seek="player_controls('seek', ...arguments)"
            >

            </item-container>

        </div>


        <div v-if="player">
            <h4>paused: {{ player.paused }}*</h4>
        </div>


        <div class="debug-container">
            <button @click="player_play_all">PLAY ALL ON PAGE</button>
            <p>
                is master: {{ is_master }} - has master: {{ has_master }}
            </p>

            <div class="controls">

                    <span @click="player_pasue">pause</span>
                    <span @click="player_resume">resume</span>
                    <span @click="player_play">play</span>
                    <span @click="player_seek">seek</span>

            </div>


            <ul>
                <li @click="player_load_from_api">player_load_from_api</li>
            </ul>

            <!--
            <div>
                <h4>heartbeat</h4>
                <div v-for="payload in heartbeat_payloads">
                    {{ payload }}<br>
                </div>
                <h4>actions</h4>
                <div v-for="payload in action_payloads">
                    {{ payload }}<br>
                </div>
            </div>
            -->

        </div>


    </div>

</template>
