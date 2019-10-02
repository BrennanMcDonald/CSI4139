/* global BigInt */
import React from "react"
import axios from "axios";
import {Link} from 'react-router-dom'
import BigInt from 'big-integer'
const values = require("./values.json");

export default class PhoneVerify extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: false, 
      err_msg: "",
      email: "",
      password: "",
      phonenumber: ""
    }
    console.log(values.g);
    console.log(values.p);
  }

  onChange(e) {
    if (e.target.name === "password"){
      var isnum = /^\d+$/.test(e.target.value);
      if (isnum || e.target.value === "") {
        this.setState({
          [e.target.name]: e.target.value
        })
      }
    } else {
      this.setState({
        [e.target.name]: e.target.value
      })
    }
  }

  createNewUser() {
    var that = this;
    var alpha = BigInt(values.g).modPow(this.state.password, values.p);
    console.log(alpha)
    console.log(values.p)
    console.log(this.state.password)
    axios.post('http://127.0.0.1:8080/api/user', null, {params: {
      email: this.state.email,
      alpha: alpha.toString(),
      phonenumber: this.state.phonenumber
    }})
      .then(function (response) {
        console.log(response);
        that.props.history.push("/")
      })
      .catch(function (error) {
        window.location.href = 'localhost:5000/api/key'

      });
  }

  render() {
    return (
      <div id="PhoneVerify" className="floating-form">
        {
          this.state.error &&
          <div>
            Error: {this.state.err_msg}
          </div>
        }
        <input name="email" placeholder="Email" onChange={this.onChange.bind(this)} value={this.state.email}></input>
        <input name="password" placeholder="Password" onChange={this.onChange.bind(this)} value={this.state.password}></input>
        <input name="phonenumber" placeholder="Phone Number" onChange={this.onChange.bind(this)} value={this.state.phonenumber}></input>
        <button id="btn" onClick={this.createNewUser.bind(this)}>Submit</button>
        <br />
        <br />
        <Link to="/">Login</Link>
      </div>
    )
  }
}