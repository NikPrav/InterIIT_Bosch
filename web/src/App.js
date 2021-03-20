import "./App.css";
import "antd/dist/antd.css";
import {Switch, Route, BrowserRouter as Router} from "react-router-dom";
import Editor from "./Components/Editor/Editor";
import Landing from "./Components/Landing/Landing";

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/editor">
            <Editor />
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
