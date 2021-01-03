import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      alive = 0,
      pp = [NaN,NaN,NaN,NaN],
      strs: [],
      user: "user",
      server: null,
      ip: "www.minesweeperme.me:8020",
    };
  }

  request(event) {
    let s=event.data.split(" ");
    let pps=[s[0],s[1],s[2],s[3]];
    let n=s[4];
    let i=0;
    let arr=[];
    for (i=0;i<n;i++){
      arr.push([s[5*i+5],s[5*i+6],s[5*i+7],s[5*i+8],s[5*i+9]].map(Number));
    }
    this.setState({
      strs: arr,
      alive: 1,
      pp: pps,
    });
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
      ws.onopen = () => ws.send('RENAME|'+this.state.user+' '+this.state.pwd);
      this.setState({server: ws});
    }
    else if (this.state.server !== null && this.state.server.readyState === 1) {
      this.state.server.send('DATABASE|'+this.state.user);
    }
  }

  renderStats(strs) {
    return strs.map((str) => {
      return (
        <p key={str[3]}>{str[3]+' pp | Board: '+str[0]+'x'+str[1]+', '+str[2]+' mines | Density: '+str[2]/(str[0]*str[1])+' | Completion: '+str[4]/(str[0]*str[1]-str[2])}%</p>
      );
    });
  }

  render() {
    return (
      <div className="game">
        <div className="leaderboard">
          <h2>Player Stats</h2>
          <p>Sum of best: {this.state.pp[0]}</p>
          <p>Weighted sum of best 10: {this.state.pp[1]}</p>
          <p>Sum of all PPs: {this.state.pp[2]}</p>
          <p>PPv2: {this.state.pp[3]}</p>
          {this.renderLeader(this.state.strs)}
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
