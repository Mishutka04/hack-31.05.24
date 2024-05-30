<template>
  <div class="row">
    <div class="col-sm-2 height">
      <div class="item_list">
        <div class="list_title">
          Маршруты
        </div>
        <div v-for="(line, index) in lines" :key='index' v-if="lines">
          <div class="item" @click="Mark_get(line.id)">
            <div>{{ line.title }}</div>
            <img src="../assets/home.png" alt="" width="27px" height="27px">
          </div>
        </div>
      </div>
    </div>

    <div class="col-sm-4 height">
      <div v-if="message" class="chat">
        <div class="chat_title">
          <div>Диалог: {{ message[0].title }}</div>
        </div>
        <div class="chat_messages" style="overflow-y:scroll;">

          <div class="left_message">
            <div class="message left">
              <div class="voice">
                <div class="play">
                  <img src="../assets/play.svg" alt="" width="50px" height="50px" @click="play(message[0].audio_file)">
                </div>
                <div class="sound">
                  <img src="../assets/sound.svg" alt="" height="50px">
                </div>

              </div>
              <div class="text">
                {{ message[0].audio_text }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="col-sm-6 height">
      <div class="result" v-if="message">
        <div class="stat_title">Результат</div>
        <div class="stat_list">
          <div class="stat_item">Название диалога - <b>{{ message[0].title }}</b></div>
          <div class="stat_item">Качество диалога - <b>{{ message[0].percentage_compliance.toFixed(1) * 100 }} %</b>
          </div>
          <div v-if="message[0].regulations_complies" class="stat_item">
            <div>Соотвествествие нормативу - <b>соотвествует</b></div>
            <div>Данный диалог не несет никакой опастности!</div>
          </div>
          <div v-else class="stat_item">Соотвествествие нормативу - <b>не соотвествует</b>
            <div class="error">
              <div class="stat_item">Комментарий к нарушению - {{ message[0].comment }}</div>
            </div>
          </div>
          <div class="stat_item">Дата - <b>{{ message[0].date }}</b></div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import { useRoute } from "vue-router";
import { useRouter } from "vue-router";
import axios from 'axios';
export default {
  data() {
    return {
      lines: null,
      message: null,
      audio_voice: null,
      chat_id: null,

    }
  },
  setup() {
    const route = useRoute();
    const router = useRouter();

    function Mark_get(id) {
      router.push('/route/' + id);
    };
    return {
      Mark_get, route
    }
  },
  methods: {
    play(path_file) {
      if (this.audio_voice) {

        console.log('stop');
        this.audio_voice.pause();
        this.audio_voice = null;

      } else {
        console.log('start');
        console.log(path_file);
        this.audio_voice = new Audio(path_file); // path to file
        this.audio_voice.play();
      }
    }
  },
  mounted() {
    axios.get(this.$globalUrl + 'api/negotiations_info/' + this.route.params.chat_id,).then(response => {
      this.message = response.data
    }),
      axios.get(this.$globalUrl + 'api/lines/').then(response => {
        this.lines = response.data;

      });
  }
}




</script>