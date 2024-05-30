<template>
    <div class="container">
        <div class="row">
            <div class="col-sm-5 height">
                <div class="category">
                    <div class="category_description">
                        <div>
                            <div class="block_title">Линии</div>
                            <div class="line"></div>
                            <div v-for="(line, index) in lines" :key='index' v-if="lines">
                                <div class="item" @click="Mark_get(line.id)">
                                    <div>{{ line.title }}</div>
                                    <img src="../assets/home.png" alt="" width="27px" height="27px">
                                </div>
                            </div>
                        </div>

                        <div class="mark_bottom">
                            <div class="line"></div>
                            <div class="container">
                                <div class="mark_content">
                                    <div class="mark_items">
                                        <div class="mark_item">
                                            <img src="../assets/yes.png" alt="yes" width="30px" height="30px">
                                            <div><b>Нарушений нет</b></div>


                                        </div>
                                        <div class="mark_item">
                                            <img src="../assets/no.png" alt="yes" width="30px" height="30px">
                                            <div><b>Нарушения</b></div>

                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            <div class="col-sm-7 height">
                <div class="graph">
                    <div class="block_title">График нарушений</div>
                    <div class="line"></div>
                    <div class="grafic">
                        <canvas id="myChart"></canvas>
                    </div>
                </div>
                <div class="stat">
                    <div class="block_title">Детальная информация</div>
                    <div class="line"></div>
                    <div class="stat_item">Качество переговоров - <b>{{ this.sr_count }} %</b></div>
                    <div class="stat_item">Количество переговоров с нарушениями - <b>{{ this.count_not_accept }}</b></div>
                    <div class="stat_item">Количество переговоров без нарушений - <b>{{ this.count_accept }}</b></div>

                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { useRouter } from "vue-router";
import axios from 'axios';
import Chart from 'chart.js/auto';
export default {
    components: {

    },
    data() {
        return {
            lines: null,
            count_accept: 0,
            count_not_accept: 0,
            sr_count: 0,
        }
    },
    setup() {
        const router = useRouter();
        function Mark_get(id) {
            console.log(id)
            router.push('/route/' + id);
        };
        return {
            Mark_get
        }
    },
    mounted() {
        axios.get(this.$globalUrl + 'api/lines/').then(response => {
            this.lines = response.data
        }),
            axios.get(this.$globalUrl + 'api/negotiations/').then(response => {
                for (let i = 0; i < response.data.length; i++) {
                    if (response.data[i].regulations_complies) {
                        this.count_accept = this.count_accept + 1;
                    } else {
                        this.count_not_accept = this.count_not_accept + 1;
                    };
                    this.sr_count = this.sr_count + response.data[i].percentage_compliance;
                };
                this.sr_count = (this.count_accept * 100 / response.data.length).toFixed(1);
            }),
            setTimeout(() => {

                new Chart(document.getElementById('myChart'), {
                    type: 'pie',
                    data: {
                        labels: ["Нарушения", "Без нарушений"],
                        datasets: [{
                            label: "Единиц",
                            backgroundColor: ["#FF3300", "#339966"],
                            data: [this.count_not_accept,this.count_accept,]
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
    },
}

</script>