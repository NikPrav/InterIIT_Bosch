import "antd/dist/antd.css";
import "./App.css";
import {Switch, Route, BrowserRouter as Router} from "react-router-dom";
import Editor from "./Components/Editor/Editor";
import Landing from "./Components/Landing/Landing";
import Home from "./Components/Home/Home";
import Trainer from "./Components/Trainer/Trainer";
import Infer from "./Components/Infer/Infer";
import {Auth0Provider} from "@auth0/auth0-react";

function App() {
  return (
    <div className="App">
      <Auth0Provider
        domain="dev-kqx4v2yr.jp.auth0.com"
        clientId="DBJyWZCoiZFCccUM5C50YYSPrBXn08oL"
        redirectUri={"http://localhost:3000/home"}
      >
        <Router>
          <Switch>
            <Route path="/editor">
              <Editor />
            </Route>
            <Route path="/home">
              <Home />
            </Route>
            <Route path="/trainer">
              <Trainer />
            </Route>
            <Route path="/infer">
              <Infer />
            </Route>
            <Route path="/">
              <Landing />
            </Route>
          </Switch>
        </Router>
      </Auth0Provider>
    </div>
  );
}

export default App;
