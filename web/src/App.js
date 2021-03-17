import "./App.css";
import "antd/dist/antd.css";
import {Switch, Route, BrowserRouter as Router} from "react-router-dom";
import Editor from "./Components/Editor/Editor";

function App() {
  return (
    <div className="App">
      <Router>
        <Switch>
          <Route path="/editor">
            <Editor />
          </Route>
        </Switch>
      </Router>
    </div>
  );
}

export default App;
