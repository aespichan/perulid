import React from 'react';
import ReactDOM from 'react-dom';
import Chart from 'chart.js'

var doughnutChart = null;

class Information extends React.Component {
  componentDidUpdate() {
    var $this = $(ReactDOM.findDOMNode(this));
    renderChart(this.props.index)
  }

  componentDidMount() {
    var $this = $(ReactDOM.findDOMNode(this));
    renderChart(this.props.index)
  }

  render() {
    const probabilities = proba[this.props.index].map((value, index) => {
      return (
        <li key={index}>{value[0]} ({value[1]}): {value[2]}%</li>
      );
    });

    var sentence = ""
    if (per_sentence){
      sentence = (<p><b>{sentences_list[this.props.index]}</b></p>)
    }

    return (
      <div>
        {sentence}
        <p>Parece ser: {pred[this.props.index]}</p>
        <ul>
          {probabilities}
        </ul>
        <div id="wrapper" width="800" height="800">
          <canvas id="probaChart"></canvas>
        </div>
      </div>
    );
  }
}

class Results extends React.Component {
  constructor() {
    super();
    this.state = {
      index: 0
    };
  }

  information(index) {
    this.setState({
      index: index,
    });
  }

  render() {

    const sentences = sentences_list.map((value, index) => {
      if (per_sentence){
        return (
          <a key={index} href="#" className="in-sentence" onClick={() => this.information(index)}>{value} </a>
        );
      } else {
        return (
          <span key={index}>{value}</span>
        );
      }
      
    });
    

    const current_index = this.state.index;

    return (
      <div className="row">
        <div className="col-lg-6" id="text">
          <p id="sentences">{sentences}</p>
        </div>
        <div className="col-lg-6" id="information">
          <Information
            index = {current_index}
          />
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(<Results />, document.getElementById("results"));

function renderChart(index) {
  var labels = []
  var probabilities = []

  var info = proba[index]
  for (var i = 0; i < info.length; i++) { 
    labels.push(info[i][1])
    probabilities.push(info[i][2])
  }

  var data = {
    datasets: [{
      data: probabilities,
      backgroundColor: ["#3e95cd", "#8e5ea2","#3cba9f","#e8c3b9","#c45850"]
    }],
    labels: labels,
  }

  if (doughnutChart) {
    doughnutChart.destroy();
  }

  var ctx = document.getElementById("probaChart");
  doughnutChart = new Chart(ctx, {
    type: 'doughnut',
    data: data
  });
}
