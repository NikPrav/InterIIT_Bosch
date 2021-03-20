import "antd/dist/antd.dark.css";
import "./App.css";
import {Switch, Route, BrowserRouter as Router} from "react-router-dom";
import Editor from "./Components/Editor/Editor";
import Landing from "./Components/Landing/Landing";
import Home from "./Components/Home/Home"

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/editor">
            <Editor />
          </Route>
          <Route path="/home">
            <Home />
          </Route>
          <Route path="/">
            <Landing />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
