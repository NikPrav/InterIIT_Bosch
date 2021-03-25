import React, {useState, useEffect} from "react";
import Navbar from "../Navbar/Navbar";
import {Layout, Header, Dropdown, Button, Typography, Menu, Card, Slider} from "antd";
import {useAuth0} from "@auth0/auth0-react";
import request from "umi-request";
import {useParams} from "react-router";

function PrefSlider(props) {
  const {max, min, step, defaultValue, stateFunction, sliderValue} = props;
  console.log(defaultValue);
  const handleChange = val => {
    stateFunction(val);
  };
  return (
    <div style={{maxWidth: "32vw", float: "right", width: "600px"}}>
      <Slider
        min={min}
        max={max}
        step={step}
        value={sliderValue}
        onChange={handleChange}
        defaultValue={defaultValue}
      />
    </div>
  );
}

function Preferences(props) {
  const {
    optimizerfn,
    setOptimizerfn,
    batchSize,
    setBatchSize,
    epochs,
    setEpochs,
    learningRate,
    setLearningRate,
    testTrainSplit,
    setTestTrainSplit,
  } = props;
  const [buttonState, setButtonState] = useState("nll_loss");

  const Simple = item => {
    <Menu.Item>{item}</Menu.Item>;
  };

  const OptimizerDropdown = (
    <Menu>
      <Menu.Item
        onClick={() => {
          setOptimizerfn("SGD");
        }}
      >
        SGD
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setOptimizerfn("ADAM");
        }}
      >
        ADAM
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setOptimizerfn("ADAGRAD");
        }}
      >
        ADAGRAD
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setOptimizerfn("RMSPROP");
        }}
      >
        RMSPROP
      </Menu.Item>
    </Menu>
  );
  return (
    <Card style={{paddingRight: "100px", paddingLeft: "100px", paddingTop: "30px"}}>
      <div>
        <p style={{fontSize: "20px"}}>
          <strong>Model Parameters</strong>
        </p>
        <p>
          <Typography.Text>Batch Size(in powers of 2):</Typography.Text>{" "}
          <PrefSlider
            defaultValue={7}
            min={4}
            max={9}
            step={1}
            sliderValue={batchSize}
            stateFunction={setBatchSize}
          />
        </p>
        <p>
          <Typography.Text>Epochs</Typography.Text>{" "}
          <PrefSlider
            defaultValue={41}
            min={1}
            max={101}
            step={10}
            sliderValue={epochs}
            stateFunction={setEpochs}
          />
        </p>
        <p>
          <Typography.Text>Learning Rate</Typography.Text>{" "}
          <PrefSlider
            defaultValue={0.5}
            min={0}
            max={1}
            step={0.1}
            sliderValue={learningRate}
            stateFunction={setLearningRate}
          />
        </p>
        <p>
          <Typography.Text>Test-Train Split</Typography.Text>{" "}
          <PrefSlider
            min={4}
            max={60}
            step={4}
            defaultValue={20}
            sliderValue={testTrainSplit}
            stateFunction={setTestTrainSplit}
          />
        </p>

        <p>
          Optimizer Function
          <Dropdown trigger={["click"]} overlay={OptimizerDropdown}>
            <Button style={{float: "right", minWidth: "11vw"}}>{optimizerfn}</Button>
          </Dropdown>
        </p>
      </div>
    </Card>
  );
}

function Trainer(props) {
  const workspace_id = 12;
  const {user, isAuthenticated, getAccessTokenSilently} = useAuth0();
  const {Header, Footer, Sider, Content} = Layout;
  const [collapsed, setcollapsed] = useState(false);
  const [selectedSection, setselectedSection] = useState(0);
  const [workspaceDetails, setWorkspaceDetails] = useState({});
  const [trained, settrained] = useState(false);
  const [trainResults, settrainResults] = useState(false);
  const [optimizerfn, setOptimizerfn] = useState("Sgd");
  const [batchSize, setBatchSize] = useState(7);
  const [epochs, setEpochs] = useState(41);
  const [learningRate, setLearningRate] = useState(0.5);
  const [testTrainSplit, setTestTrainSplit] = useState(20);

  const collapseToggle = () => {
    setcollapsed(!collapsed);
  };

  const getWorkSpaceDetails = async () => {
    try {
      const localaccessToken = await getAccessTokenSilently({
        audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
        scope: "read:current_user",
      });

      const userWorkSpaceReq = await request(
        `${process.env.REACT_APP_API_URL}/workspaces/${workspace_id}`,
        {
          method: "patch",
          headers: {
            Authorization: `Bearer ${localaccessToken}`,
            email: `${user.email}`,
          },
        }
      );
      const umimessage = await userWorkSpaceReq;

      console.log(umimessage);
      setWorkspaceDetails(umimessage);
    } catch (e) {
      console.log(e.message);
    }
  };

  useEffect(
    async user => {
      console.log("Grab Workspace Details");
      await getWorkSpaceDetails();
    },
    [user]
  );

  const updateModelParams = async () => {
    try {
      const localaccessToken = await getAccessTokenSilently({
        audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
        scope: "read:current_user",
      });

      const updateRequest = await request(
        `${process.env.REACT_APP_API_URL}/workspaces/${workspace_id}/rpc/setModelParams`,
        {
          method: "patch",
          headers: {
            Authorization: `Bearer ${localaccessToken}`,
            email: `${user.email}`,
          },
          data: {
            name: workspace_id,
            l: learningRate,
            t: testTrainSplit,
            e: Math.pow(2, epochs),
          },
        }
      );
      const umimessage = await updateRequest;
      console.log(umimessage);
    } catch (e) {
      console.log(e.message);
    }
  };

  const trainRequest = async () => {
    try {
      const localaccessToken = await getAccessTokenSilently({
        audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
        scope: "read:current_user",
      });

      const trainRequest = await request(
        `${process.env.REACT_APP_API_URL}/workspaces/${workspace_id}/rpc/startTrain`,
        {
          method: "post",
          headers: {
            Authorization: `Bearer ${localaccessToken}`,
            email: `${user.email}`,
          },
        }
      );
      const umimessage = await trainRequest;
      console.log(umimessage);
    } catch (e) {
      console.log(e.message);
    }
  };
  return (
    <Layout className="main_container">
      <Header className="header">
        <Navbar activePage="2" />
      </Header>
      <Layout>
        <Content style={{margin: "50px", padding: "20px"}}>
          <Card style={{minHeight: "60vh"}}>
            <Preferences
              optimizerfn={optimizerfn}
              setOptimizerfn={setOptimizerfn}
              batchSize={batchSize}
              epochs={epochs}
              setEpochs={setEpochs}
              learningRate={learningRate}
              setLearningRate={setLearningRate}
              testTrainSplit={testTrainSplit}
            />
            <Button
              type="primary"
              style={{float: "right", marginRight: "7em", minWidth: "11vw", marginTop: "10px"}}
              onClick={async () => {
                await updateModelParams();
                await trainRequest();
                settrained(true);
              }}
            >
              {trained ? "Retrain Model" : "Train Model"}
              {trained && (
                <p>
                  <br />
                  Training has finished. You can now visit the inference section to infer images
                </p>
              )}
            </Button>
          </Card>
        </Content>
      </Layout>
      <Footer></Footer>
    </Layout>
  );
}

export default Trainer;
