import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      alive: 0,
      pp: [NaN,NaN,NaN,NaN],
      strs: [],
      tops: [],
      user: "user",
      server: null,
      ip: "www.minesweeperme.me:8020",
    };
    this.updateUser = this.updateUser.bind(this);
    this.updateIP = this.updateIP.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  request(event) {
    let s=event.data.split(" ");
    if (s[0]==='DATABASE') {
    let pps=[s[1],s[2],s[3],s[4]];
    let n=s[5];
    let i=0;
    let arr=[];
    for (i=0;i<n;i++){
      arr.push([]);
      arr[i].push([s[5*i+6],s[5*i+7],s[5*i+8],s[5*i+9],s[5*i+10]].map(Number));
      arr[i].push(1000000000+i);
    }
    this.setState({
      strs: arr,
      pp: pps,
    });
    }
    else {
    let n=s[1];
    let i=0;
    let arr=[];
    for (i=0;i<n;i++){
      arr.push([]);
      arr[i].push([s[6*i+2],s[6*i+3],s[6*i+4],s[6*i+5],s[6*i+6],s[6*i+7]]);
      arr[i].push(2000000000+i);
    }
    this.setState({
      tops: arr
    });
    }
  }

  updateUser(e) {
    this.setState({user: e.target.value});
  }

  updateIP(e) {
    this.setState({ip: e.target.value});
  }

  handleSubmit(e) {
    e.preventDefault();
    if (this.state.alive === 0){
      const ws = new WebSocket("ws://"+this.state.ip);
      ws.onmessage = (e) => this.request(e);
      ws.onopen = () => {
        this.setState({alive: 1});
        ws.send('TOP_PP_PLAYS|');
      }
      this.setState({server: ws});
    }
    else if (this.state.server !== null && this.state.server.readyState === 1) {
      this.state.server.send('DATABASE|'+this.state.user);
    }
  }

  renderStats(strs) {
    return strs.map((str) => {
      return (
        <p key={str[1]}>{str[0][3]+' pp | Board: '+str[0][0]+'x'+str[0][1]+', '+str[0][2]+' mines | Density: '+(str[0][2]/(str[0][0]*str[0][1])).toFixed(2)+' | Completion: '+(100*str[0][4]/(str[0][0]*str[0][1]-str[0][2])).toFixed(2)}%</p>
      );
    });
  }

  renderTops(strs) {
    return strs.map((str) => {
      return (
        <p key={str[1]}>{str[0][4]+' pp | '+str[0][0]+' | Board: '+str[0][1]+'x'+str[0][2]+', '+str[0][3]+' mines | Density: '+(Number(str[0][3])/(Number(str[0][1])*Number(str[0][2]))).toFixed(2)+' | Completion: '+(100*Number(str[0][5])/(Number(str[0][1])*Number(str[0][2])-Number(str[0][3]))).toFixed(2)}%</p>
      );
    });
  }

  render() {
    return (
      <div className="game">
        <div className="leaderboard">
          <h2>Player Stats</h2>
          <p>Sum of best: {this.state.pp[0]}</p>
          <p>Sum of best 10: {this.state.pp[1]}</p>
          <p>Sum of all PPs: {this.state.pp[2]}</p>
          <p>PPv2: {this.state.pp[3]}</p>
          {this.renderStats(this.state.strs)}
        </div>
        <div className="top-plays">
          <h2>Highest pp plays</h2>
          {this.renderTops(this.state.tops)}
        </div>
        <div className="user-info">
          <form onSubmit={this.handleSubmit}>
            <label>
              Server IP: 
              <input type="text" value={this.state.ip} onChange={this.updateIP} />
            </label>
            <br></br>
            <label>
              Username: 
              <input type="text" value={this.state.user} onChange={this.updateUser} />
            </label>
            <input type="submit" value="Submit" />
          </form>
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(<Game />, document.getElementById("root"));
