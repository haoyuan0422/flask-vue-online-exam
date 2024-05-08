<!-- 考试成绩分段统计图 -->
<template>
  <div>
    <section class="description">
      <p class="title">成绩统计图介绍</p>
      <p class="content">饼状图反馈的是参与目标考试的成绩分段情况，图表绘制稍有粗糙，后续会进行改进。</p>
    </section>
    <div class="part" >
      <div class="box" ref="box"></div>
      <div class="notFound" v-if="isNull">
          <i class="iconfont icon-LC_icon_tips_fill"></i><span>还无学生参与该考试哦，请提醒学生准时参加考试</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      isNull: false, //是否有成绩标志位
      name: null,
      category: { //保存分数段
        '90分及以上': 0,
        '80-89分': 0,
        '70-79分': 0,
        '60-69分': 0,
        '60分以下': 0,
      }
    }
  },
  created() {
    this.getScoreInfo()

  },
  methods: {
    getScoreInfo() {
      let examCode = this.$route.query.examCode
      this.name = this.$route.query.source
      this.$axios(`/teacher/scores/${examCode}`).then(res => {
        let data = res.data.data
        if(res.data.data.length!=0) {//数据不为空
          let box = this.$refs['box']
          let charts = this.$echarts.init(box)
          data.forEach(element => {
            switch(element.etScore / 10) {
              case 10:
              case 9:
                this.category["90分及以上"]++
                break
              case 8:
                this.category['80-89分']++
                break
              case 7:
                this.category["70-79分"]++
                break
              case 6:
                this.category['60-69分']++
                break
              default:
                this.category['60分以下']++
            }
          });
          let option = {
              title : {
                  text: `${this.name}——分数段图`,
                  subtext: '分数段饼图',
                  x:'center'
              },
              tooltip : {
                  trigger: 'item',
                  formatter: "{a}：{b} <br/> {c}人 ({d}%)"
              },
              legend: {
                  orient: 'vertical',
                  left: 'left',
                  data: ['90分及以上','80-89分','70-79分','60-69分','60分以下']
              },
              series : [
                  {
                      name: '分数段',
                      type: 'pie',
                      radius : '35%',
                      center: ['50%', '35%'],
                      data:[
                          {value:this.category['90分及以上'], name:'90分及以上'},
                          {value:this.category['80-89分'], name:'80-89分'},
                          {value:this.category['70-79分'], name:'70-79分'},
                          {value:this.category['60-69分'], name:'60-69分'},
                          {value:this.category['60分以下'], name:'60分以下'}
                      ],
                      itemStyle: {
                          emphasis: {
                              shadowBlur: 10,
                              shadowOffsetX: 0,
                              shadowColor: 'rgba(0, 0, 0, 0.5)'
                          }
                      }
                  }
              ]
          };
          charts.setOption(option)
        }else {
          this.isNull = true
        }
      })
    }
  },

}
</script>

<style lang="less" scoped>
.part {
  .box {
    width: 800px;
    height: 800px;
    margin-left: 40px;
  }
  .notFound {
    position: absolute;
    top: 300px;
    left: 300px;
  }
}
.description {
  margin-left: 40px;
  .title {
    font-size: 22px;
    font-weight: 400;
    color: rgb(31, 47, 61);
  }
  .content {
    width: 700px;
    background-color: #FAF5F2;
    padding: 16px 32px;
    border-radius: 4px;
    border-left: 5px solid #FDC8C8;
    margin: 20px 0px;
  }
}
</style>


