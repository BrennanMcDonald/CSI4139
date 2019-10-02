import React from 'react';
import firebase from 'firebase/app';
import { BrowserRouter as Router, Route } from "react-router-dom";

import EmailInput from './EmailInput'
import AddUser from "./AddUser"

import "./setupProxy"
import 'firebase/auth'
import './App.css';

const firebaseConfig = {
  apiKey: "AIzaSyDiHmms0XCJRHhzMzUJDUz1G1NwLNWbRjM",
  authDomain: "csi4139-lab2.firebaseapp.com",
  databaseURL: "https://csi4139-lab2.firebaseio.com",
  projectId: "csi4139-lab2",
  storageBucket: "",
  messagingSenderId: "922993488222",
  appId: "1:922993488222:web:4f341d6d1e0a223c3f1fcf"
};

firebase.initializeApp(firebaseConfig);

console.warn = function(){}
console.info = function(){}

class App extends React.Component {
  render() {
    return (
      <div className="container">
      <Router>
        <Route path="/" exact component={EmailInput} />
        <Route path="/register" component={AddUser} />
      </Router>

      </div>
    );
  }
}

export default App;
