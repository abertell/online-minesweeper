import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      boardData: [[["!",0,-1]]],
      boardX: 0,
      boardY: 0,
      mines: 0,
      score: 0,
      strs: [],
      user: "user",
      pwd: "pwd",
      id: "roomID",
      ip: "localhost:8000",
      alive: 3,
      server: null,
    };
    console.log(this.state.server);
    this.updateUser = this.updateUser.bind(this);
    this.updatePwd = this.updatePwd.bind(this);
    this.updateID = this.updateID.bind(this);
    this.updateIP = this.updateIP.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  request(event) {
    let s=event.data.split(" ");
    let x=Number(s[0]);
    let y=Number(s[1]);
    let m=Number(s[2]);
    let sc=Number(s[3]);
    let stat=Number(s[4]);
    let v=Number(s[5]);
    let strs = [];
    let i=0;
    for (i=0;i<v;i++){
      strs.push([]);
      strs[i].push([s[6+3*i],s[7+3*i],["DEAD","ALIVE"][Number(s[8+3*i])]]);
      strs[i].push(1000000000+i);
    }
    let res = [];
    i=0;
    let j=0;
    for (i=0;i<y;i++) {
      res.push([]);
      for (j=0;j<x;j++) {
        let val=s[6+2*v+i*x+j];
        if (val==="-1") {
          val="▮";
        }
        else if (val==="0") {
          val=" ";
        }
        else if (val==="F") {
          val="►";
        }
        else if (val==="G") {
          val="▷";
        }
        else if (val==="M") {
          val="X";
        }
        res[i].push([val,i,j]);
      }
    }
    this.setState({
      boardData: res,
      boardX: x,
      boardY: y,
      mines: m,
      score: sc,
      strs: strs,
      alive: stat,
    });
  }

  sendClick(x,y) {
    if (this.state.server.readyState === 1) {
      this.state.server.send('MOVE|'+x+' '+y);
    }
  }

  sendFlag(e,x,y) {
    e.preventDefault();
    if (this.state.server.readyState === 1) {
      this.state.server.send('FLAG|'+x+' '+y);
    }
    return false;
  }

  updateUser(e) {
    if (this.state.alive === 3) {
      this.setState({user: e.target.value});
    }
  }

  updatePwd(e) {
    if (this.state.alive === 3) {
      this.setState({pwd: e.target.value});
    }
  }

  updateID(e) {
    this.setState({id: e.target.value});
  }

  updateIP(e) {
    this.setState({ip: e.target.value});
  }

  handleSubmit(e) {
    e.preventDefault();
    if (this.state.alive === 3){
      const ws = new WebSocket("ws://"+this.state.ip);
      ws.onmessage = (e) => this.request(e);
      ws.onopen = () => ws.send('RENAME|'+this.state.user+' '+this.state.pwd);
      this.setState({server: ws});
    }
    else if (this.state.server.readyState === 1) {
      this.state.server.send('JOIN ROOM|'+this.state.id);
    }
  }

  renderRow(datarow) {
    return datarow.map((dataitem) => {
      return (
        <button
          key={dataitem[2] * this.state.boardX + dataitem[1]}
          className="square"
          onClick={() => this.sendClick(dataitem[1],dataitem[2])}
          onContextMenu={(e) => this.sendFlag(e,dataitem[1],dataitem[2])}
        >
          {dataitem[0]}
        </button>
      );
    });
  }

  renderBoard(data) {
    return data.map((datarow) => {
      return (
        <div key={-datarow[0][1]}>
          {this.renderRow(datarow)}
        </div>
      );
    });
  }

  renderLeader(strs) {
    return strs.map((str) => {
      return (
        <p key={str[1]}>{str[0][0]+': '+str[0][1]+' | '+str[0][2]}</p>
      );
    });
  }

  render() {
    return (
      <div className="game">
        <div className="game-board">
          {this.renderBoard(this.state.boardData)}
        </div>
        <div className="game-info">
          You are {["dead", "alive", "not in a room", "not connected"][this.state.alive]}.
          <br></br>
          Score: {this.state.score}
          <br></br>
          Mines left: {this.state.mines}
        </div>
        <div className="leaderboard">
          <h2>Leaderboard</h2>
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
            <br></br>
            <label>
              Password: 
              <input type="text" value={this.state.pwd} onChange={this.updatePwd} />
            </label>
            <br></br>
            <label>
              Room ID: 
              <input type="text" value={this.state.id} onChange={this.updateID} />
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