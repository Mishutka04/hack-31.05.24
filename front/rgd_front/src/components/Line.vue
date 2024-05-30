<template>
    <div class="row">
        <div class="col-sm-2 height">
            <div class="item_list">
                <div class="list_title">
                    <div>Маршруты</div>
                </div>
                <div class="list_messages" v-if="lines">
                    <div v-for="(line, index) in lines" :key='index'>
                        <div class="item" @click="Mark_get(line.id)">
                            <div>{{ line.title }}</div>
                            <img src="../assets/home.png" alt="" width="27px" height="27px">
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-sm-4 height">
            <div class="chat_message">
                <div class="list_title">
                    <div>Диалоги</div>
                </div>
                <div class="list_messages">
                    <div v-for="(dial, index) in dialog" :key='index' v-if="lines" class="item"
                        @click="Item_get(dial.id)">

                        <div>{{ dial.title }}</div>
                        <div v-if="dial.regulations_complies"><img src="../assets/yes.png" alt="yes" width="30px"
                                height="30px"></div>
                        <div v-else><img src="../assets/no.png" alt="yes" width="30px" height="30px"></div>
                    </div>
                </div>
            </div>

        </div>
        <div class="col-sm-6 height">
            <div class="result">
                <div class="stat_title">Результат</div>
                <div class="stat_item">Качество переговоров - <b>{{ this.sr_count }} %</b></div>
                <div class="stat_item">Качество нарушений - <b>{{ this.count_not_accept }}</b></div>
                <div class="stat_item">Качество переговоров без нарушений - <b>{{ this.count_accept }}</b></div>
                <div class="grafic">
                    <canvas id="myChart"></canvas>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useRouter } from "vue-router";
import { useRoute } from "vue-router";
import axios from 'axios';
import Chart from 'chart.js/auto';
export default {
    data() {
        return {
            lines: null,
            dialog: null,
            count_accept: 0,
            count_not_accept: 0,
            sr_count: 0,
        }
    },
    setup() {
        const router = useRouter();
        const route = useRoute();
        function Mark_get(id) {
            router.push('/route/' + id);
        };
        function Item_get(id) {
            router.push('/route/' + route.params.category_id + '/chat/' + id);
        };
        return {
            Mark_get, Item_get, route
        }
    },
    mounted() {
        axios.get(this.$globalUrl + 'api/negotiations/' + this.route.params.category_id).then(response => {
            this.dialog = response.data;
            for (let i = 0; i < this.dialog.length; i++) {
                if (this.dialog[i].regulations_complies) {
                    this.count_accept = this.count_accept + 1;
                } else {
                    this.count_not_accept = this.count_not_accept + 1;
                };
                this.sr_count = this.sr_count + this.dialog[i].percentage_compliance;
            };
            this.sr_count = (this.count_accept * 100 / this.dialog.length).toFixed(1);
        }),
            axios.get(this.$globalUrl + 'api/lines/').then(response => {
                this.lines = response.data;

            }),
            setTimeout(() => {

                new Chart(document.getElementById('myChart'), {
                    type: 'pie',
                    data: {
                        labels: ["Нарушения", "Без нарушений"],
                        datasets: [{
                            label: "Единиц",
                            backgroundColor: ["#FF3300", "#339966"],
                            data: [this.count_not_accept, this.count_accept]
                        }]
                    },
                    options: {
                        title: {
                            display: true,
                            text: 'Predicted world population (millions) in 2050'
                        },
                        responsive: true,

                    }
                })
            }, 1000);
        console.log(this.count_accept);
    },

}

</script>