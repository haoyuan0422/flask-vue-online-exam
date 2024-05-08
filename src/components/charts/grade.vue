// 成绩统计页面
<template>
  <div>
    <section class="description">
      <p class="title">成绩统计图介绍</p>
      <p class="content">折线图反馈的是目标学生参与所有考试的考试成绩，以分析该学生的学习情况，图表绘制稍有粗糙，后续会进行改进。</p>
    </section>
    <div id="grade">
      <div ref="box" class="box"></div>
      <div class="notFound" v-if="isNull">
        <i class="iconfont icon-LC_icon_tips_fill"></i><span>该考生未参加过任何考试，无成绩数据</span>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  // let boxDom = this.$refs.box,
  name: "grade",
  data() {
    return {
      isNull: false, //原始数据
      tableDataX: [], //x轴数据 保存次数
      tableDataY: [], //y轴数据 保存分数
    }
  },
  mounted() {
    this.score();
  },
  methods: {
    score() {
      let studentId = this.$route.query.studentId
      this.$axios(`/score/${studentId}`).then(res => { //根据学生Id查询成绩
        console.log(studentId)
        console.log("成功")
        // console.log(res.data.data.length)
        if(res.data.data.length!=0) {//数据不为空
          let rootData = res.data.data
          console.log(rootData)
          rootData.forEach((element,index) => {
            console.log(element.exam_name)
            console.log(index)
            this.tableDataX.push(`第${index + 1}次:`+element.exam_name)
            this.tableDataY.push(element.exam_score)
          });
          let boxDom = this.$refs["box"];
          let scoreCharts = this.$echarts.init(boxDom);
          let option = {
            xAxis: {
              type: "category",
              data: this.tableDataX
            },
            yAxis: {
              type: "value"
            },
            series: [
              {
                data: this.tableDataY,
                type: "line",
                itemStyle: { normal: { label: { show: true } } }
              }
            ]
          };
          scoreCharts.setOption(option,true);
          scoreCharts.on("mouseover", params => {
            console.log(params.value);
          });
        }else {
          console.log("失败")
          this.isNull = true
        }
      })
    }
  }
};
</script>

<style lang="less" scoped>
#grade {
  position: relative;
  .box{
    width: 1000px;
    height: 400px;
  }
  .notFound {
    position: absolute;
    top: 0px;
    left: 50px;
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
    width: 900px;
    background-color: #FAF5F2;
    padding: 16px 32px;
    border-radius: 4px;
    border-left: 5px solid #FDC8C8;
    margin: 20px 0px;
  }
}
</style>
