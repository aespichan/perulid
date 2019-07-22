import React from 'react';
import ReactDOM from 'react-dom';

const sentences_per_page = 5

class Information extends React.Component {

  constructor() {
    super();
    this.state = {
      index: 0
    };
  }

  previous(){
    if (this.state.index-1 >= 0){
      this.setState({
        index: this.state.index-1,
      });
    }
  }

  next(){
    if ((this.state.index+1)*sentences_per_page < this.props.sentences.length){
      this.setState({
        index: this.state.index+1,
      });
    }
  }

  componentWillReceiveProps(nextProps) {
    this.setState({ index: 0 });
  }

  render() {
    var results = (<p className="text-center">No se encontraron resultados</p>);

    if (this.props.sentences.length > 0){
      var start = this.state.index*sentences_per_page;
      var end = (this.state.index+1)*sentences_per_page;
      if (end > this.props.sentences.length){
        end = this.props.sentences.length
      }

      var curr_sentences = this.props.sentences.slice(start, end);
      const stcs = curr_sentences.map((value, index) => {
        var str = value.sentence.trim().split(" ");
        str[value.position] = "<b>"+str[value.position]+"</b>";
        str = str.join(" ")
        return (
          <li className="search-list-item" key={index}>
            <p className="search-sentence" dangerouslySetInnerHTML={{ __html: str }}></p>
            <p className="search-sentence">Lengua: {value.language}</p>
            <p className="search-sentence">Fuente: <a href={value.url} target="_blank">{value.url}</a></p>
          </li>
        );
      });

      var prev_disabled = "";
      if (this.state.index-1 < 0){
        prev_disabled = "disabled";
      }

      var next_disabled = "";
      if ((this.state.index+1)*sentences_per_page >= this.props.sentences.length){
        next_disabled = "disabled"
      }

      results = (
        <div>
          <ul className="search-results">{stcs}</ul>
          <div className="pull-left">
            <p>Resultados: {start+1} a {end} de {this.props.sentences.length}</p>
          </div>
          <div className="pull-right">
            <button className={'btn btn-xs btn-primary ' + prev_disabled} type="button" onClick={() => this.previous()}>
              Anterior
            </button>
            <button className={'btn btn-xs btn-primary ' + next_disabled} type="button" onClick={() => this.next()}>
              Siguiente
            </button>
          </div>
        </div>
      );
    }
    

    return (
      <div>
        {results}
      </div>
    );
  }
}

class Searcher extends React.Component {
  constructor() {
    super();
    this.state = {
      sentences: []
    };
  }

  information() {
    var search_input = $("#search_input").val().toLowerCase();

    $.ajax({
      url : "/ajax/search_sentences/",
      type: "POST",
      data : {
        'search_input': search_input
      },
      success: (res) => {
        this.setState({
          sentences: res.data,
        });
      },
      error: (res) => {
        this.setState({
          sentences: [],
        });
      }
    });

  }

  render() {
    const current_sentences = this.state.sentences;

    return (
      <div className="row">
        <div className="col-lg-12">
          <div className="row">
            <div className="col-lg-8 mx-auto" id="search">
              <p>Ingresa una palabra y la buscaremos entre nuestro repositorio de oraciones 
              en lenguas originarias peruanas. Así, podrás ver en que contextos se usa, así 
              como la fuente de donde conseguimos cada oración.</p>
              <div className="input-group">
                <input type="text" className="form-control" id="search_input" placeholder="Escribe una palabra..."/>
                <span className="input-group-btn">
                  <button className="btn btn-primary" type="button" onClick={() => this.information()}>
                    <i className="fa fa-search"></i>
                  </button>
                </span>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-lg-8 mx-auto" id="section_search_results">
              <Information
                sentences = {current_sentences}
              />
            </div>
          </div>
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(<Searcher />, document.getElementById("searcher"));
