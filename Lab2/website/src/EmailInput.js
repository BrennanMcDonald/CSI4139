import React from "react"
import axios from 'axios'
import firebase from 'firebase/app';

import "./setupProxy"
import 'firebase/auth'
import './App.css';

import { Link } from 'react-router-dom'

export default class EmailInput extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      email: "",
      error: false,
      err_msg: "",
      loading: false,
      step: 1,
      final_code: ""
    }
  }

  onChange(e) {
    this.setState({
      [e.target.name]: e.target.value
    })
  }
  componentDidMount() {
    window.recaptchaVerifier = new firebase.auth.RecaptchaVerifier('btn', {
      'size': 'invisible',
      'callback': function (response) {
        console.log("Callback");
      }
    });
  }

  sendPhoneCode() {
    this.setState({
      loading: true
    })
    var that = this;
    axios.get('/api/sendCode', {
      params: {
        email: this.state.email
      }
    }).then(res => {
      that.setState({
        step: 2
      })
      console.log(res);
    }).catch(err => {
      console.log(err);
      that.setState({
        error: true,
        loading: false,
        err_msg: "Unable to find user."
      })
    })
  }

  verifyAliceCode() {
    var that = this;
    axios.get('/api/login', {
      params: {
        email: this.state.email,
        m1: this.state.m1
      }
    }).then(res => {
      that.setState({
        step: 3,
        final_code: res.data
      })
    }).catch(err => {
      console.log(err);
      that.setState({
        error: true,
        loading: false,
        err_msg: err.response.data
      })
    })
  }

  render() {
    return (
      <div id="EmailInput" className="floating-form">
        {
          this.state.error &&
          <div className="error">
            Error: {this.state.err_msg}
          </div>
        }
        {
          this.state.step < 3 &&
          <input name="email" type="email" placeholder="Email" onChange={this.onChange.bind(this)}></input>
        }
        {
          this.state.step === 2 &&
          <input name="m1" placeholder="Digested Code" onChange={this.onChange.bind(this)}></input>
        }
        {
          this.state.step === 1 &&
          <button id="btn" onClick={this.sendPhoneCode.bind(this)}>Send Code</button>
        }
        {
          this.state.step === 2 &&
          <button id="btn" onClick={this.verifyAliceCode.bind(this)}>Submit</button>
        }
        {
          this.state.step === 3 &&
          <div>
            <p style={{color:"black", wordBreak: "break-all"}}>{this.state.final_code}</p>
          </div>
        }
        <br />
        <br />
        <Link to="/register">Create User</Link>
      </div>
    )
  }
}