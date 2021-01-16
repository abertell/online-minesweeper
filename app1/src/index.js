import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';

class Game extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      boardData: [[[]]],
      boardX: 0,
      boardY: 0,
      mines: 0,
      score: 0,
      strs: [],
	  waitingForRoom: 0,
      user: "user",
      pwd: "",
      id: "roomID",
      ip: "www.minesweeperme.me:8020",
      alive: 4,
      server: null,
      reqX: 30,
      reqY: 24,
      reqMines: 180,
      newID: "-",
      top: [],
    };
    console.log(this.state.server);
    this.updateUser = this.updateUser.bind(this);
    this.updatePwd = this.updatePwd.bind(this);
    this.updateID = this.updateID.bind(this);
    this.updateIP = this.updateIP.bind(this);
    this.updateReqX = this.updateReqX.bind(this);
    this.updateReqY = this.updateReqY.bind(this);
    this.updateReqMines = this.updateReqMines.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
    this.makeRoomAndWait = this.makeRoomAndWait.bind(this);
  }

  request(event) {
    let s=event.data.split(" ");
    if (s[0]==="Error") {
      alert(s[1]);
      return 1;
    }
    if (s[0]==="USER_LEADER_PPV2") {
      let ll=s[1];
      let i=0;
      let arr=[];
      for (i=0;i<ll;i++){
        arr.push([]);
        arr[i].push([s[2+2*i],s[3+2*i]]);
        arr[i].push(2000000000+i);
      }
      this.setState({top: arr});
      return 0;
    }
    else {
    let newid=s[1];
    let x=Number(s[2]);
    let y=Number(s[3]);
    let m=Number(s[4]);
    let sc=Number(s[5]);
    let stat=Number(s[6]);
    let v=Number(s[7]);
    let pre = 8;
    let len = 4;
    let strs = [];
    let i=0;
	
	if (newid !== '-' && this.state.waitingForRoom === 1){
	  this.setState({waitingForRoom: 0});
	  this.setState({id: newid});
	  this.state.server.send('JOIN_ROOM|'+this.state.id);
	  return 0;
    }
	
    for (i=0;i<v;i++){
      strs.push([]);
      strs[i].push([s[pre+len*i],s[pre+1+len*i],["DEAD","ALIVE","WON"][Number(s[pre+2+len*i])],s[pre+3+len*i]]);
      strs[i].push(1000000000+i);
    }
    let res = [];
    i=0;
    let j=0;
    for (i=0;i<y;i++) {
      res.push([]);
      for (j=0;j<x;j++) {
        let val=s[pre+4*v+i*x+j];
        if (val==="-1") {
          val=".";
        }
        else if (val==="0") {
          val=" ";
        }
        else if (val==="F") {
          val="🔺";
        }
        else if (val==="G") {
          val="△";
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
  }

  sendClick(x,y) {
    if (this.state.server !== null && this.state.server.readyState === 1) {
      this.state.server.send('MOVE|'+x+' '+y);
    }
  }

  sendFlag(e,x,y) {
    e.preventDefault();
    if (this.state.server !== null && this.state.server.readyState === 1) {
      this.state.server.send('FLAG|'+x+' '+y);
    }
    return false;
  }

  updateUser(e) {
    if (this.state.alive === 4) {
      this.setState({user: e.target.value});
    }
  }

  updatePwd(e) {
    if (this.state.alive === 4) {
      this.setState({pwd: e.target.value});
    }
  }

  updateID(e) {
    this.setState({id: e.target.value});
  }

  updateIP(e) {
    this.setState({ip: e.target.value});
  }

  updateReqX(e) {
    this.setState({reqX: e.target.value});
  }

  updateReqY(e) {
    this.setState({reqY: e.target.value});
  }

  updateReqMines(e) {
    this.setState({reqMines: e.target.value});
  }

  handleSubmit(e) {
    e.preventDefault();
    if (this.state.alive === 4){
      const ws = new WebSocket("ws://"+this.state.ip);
      ws.onmessage = (e) => this.request(e);
      ws.onopen = () => {
        ws.send('RENAME|'+this.state.user+' '+this.state.pwd);
        ws.send('USER_LEADER_PPV2|');
      }
      this.setState({server: ws});
    }
    else if (this.state.server !== null && this.state.server.readyState === 1) {
      this.state.server.send('JOIN_ROOM|'+this.state.id);
    }
  }
  
  makeRoomAndWait(e) {
    e.preventDefault();
    if (this.state.server !== null && this.state.server.readyState === 1) {
      this.state.server.send('CREATE_ROOM|'+this.state.reqX+' '+this.state.reqY+' '+this.state.reqMines);
	  this.setState({waitingForRoom: 1});
    }
  }

  renderRow(datarow) {
    return datarow.map((dataitem) => {
      let color="white";
      if (dataitem[0]==='.' || dataitem[0]==='🔺') {
        color="black";
      }
      else if (dataitem[0]==='X') {
        color="red";
      }
      else if (dataitem[0]==='△') {
        color="grey";
      }
      return (
        <button
          key={dataitem[2] * this.state.boardX + dataitem[1]}
          className={"square-"+color}
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
        <p key={str[1]}>{str[0][0]+': '+str[0][1]+' | '+str[0][2]+' | '+str[0][3]+'pp'}</p>
      );
    });
  }

  renderTop(strs) {
    return strs.map((str) => {
      return (
        <p key={str[1]}>{str[0][0]+' | '+str[0][1]+'pp'}</p>
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
          You {["died.", "are playing.", "won!", "are not in a room.", "are not connected."][this.state.alive]}
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
              <input type="password" value={this.state.pwd} onChange={this.updatePwd} />
            </label>
            <br></br>
            <label>
              Room ID: 
              <input type="text" value={this.state.id} onChange={this.updateID} />
            </label>
            <br></br>
            <input type="submit" value="Submit" />
          </form>
        </div>
        <div className="new-room">
          <form onSubmit={this.makeRoomAndWait}>
            <label>
              Width:
              <input type="text" value={this.state.reqX} onChange={this.updateReqX} />
            </label>
            <br></br>
            <label>
              Height:
              <input type="text" value={this.state.reqY} onChange={this.updateReqY} />
            </label>
            <br></br>
            <label>
              Mines:
              <input type="text" value={this.state.reqMines} onChange={this.updateReqMines} />
            </label>
            <br></br>
            <input type="submit" value="Create and Join" />
          </form>
          <br></br>
          <a href="https://www.minesweeperme.me/board/">Stats Page</a>
        </div>
        <div className="top-players">
          <h2>Player Rankings</h2>
          {this.renderTop(this.state.top)}
        </div>
      </div>
    );
  }
}

// ========================================

ReactDOM.render(<Game />, document.getElementById("root"));
