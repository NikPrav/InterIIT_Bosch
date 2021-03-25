import React, {useState, useEffect} from "react";
import Navbar from "../Navbar/Navbar";
import {Layout, Header, Dropdown, Button, Typography, Menu, Card, Slider} from "antd";
import {useAuth0} from "@auth0/auth0-react";
import request from "umi-request";

function PrefSlider(props) {
  const {max, min, step, defaultValue} = props;
	console.log(defaultValue)
  const [sliderValue, setSliderValue] = useState(defaultValue);
  const handleChange = val => {
    setSliderValue(val);
  };
  return (
    <div style={{maxWidth: "32vw", float: "right", width: "600px"}}>
      <Slider min={min} max={max} step={step} value={sliderValue} onChange={handleChange} defaultValue={defaultValue} />
    </div>
  );
}

function Preferences() {
  const [buttonState, setButtonState] = useState("nll_lossfunction");
  const [optimizerfn, setoptimizerfn] = useState("Sgd");

  const Simple = item => {
    <Menu.Item>{item}</Menu.Item>;
  };
  const LossFnDropdown = (
    <Menu>
      <Menu.Item
        onClick={() => {
          setButtonState("CategoricalCrossEntropy");
        }}
      >
        CategoricalCrossEntropy
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setButtonState("MeanSquaredError");
        }}
      >
        MeanSquaredError
      </Menu.Item>
    </Menu>
  );
  const OptimizerDropdown = (
    <Menu>
      <Menu.Item
        onClick={() => {
          setoptimizerfn("SGD");
        }}
      >
        SGD
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setoptimizerfn("ADAM");
        }}
      >
        ADAM
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setoptimizerfn("ADAGRAD");
        }}
      >
        ADAGRAD
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setoptimizerfn("RMSPROP");
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
          <Typography.Text>Batch Size(in powers of 2):</Typography.Text> <PrefSlider defaultValue={7} min={4} max={9} step={1} />
        </p>
        <p>
          <Typography.Text>Epochs</Typography.Text> <PrefSlider defaultValue={41} min={1} max={101} step={10} />
        </p>
        <p>
          <Typography.Text>Learning Rate</Typography.Text> <PrefSlider defaultValue={0.5} min={0} max={1} step={0.1} />
        </p>
        <p>
          <Typography.Text>Test-Train Split</Typography.Text>{" "}
          <PrefSlider min={4} max={60} step={4} defaultValue={20}/>
        </p>
        <p>
          Loss Function
          <Dropdown trigger={["click"]} overlay={LossFnDropdown}>
            <Button type="disabled" style={{float: "right", minWidth: "11vw"}}>
              {buttonState}
            </Button>
          </Dropdown>
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

function Trainer() {
  const {user, isAuthenticated, getAccessTokenSilently} = useAuth0();
  const {Header, Footer, Sider, Content} = Layout;
  const [collapsed, setcollapsed] = useState(false);
  const [selectedSection, setselectedSection] = useState(0);
  const [workspaceDetails, setWorkspaceDetails] = useState({});
  const [trained, settrained] = useState(false);
  const [trainResults, settrainResults] = useState(false);

  const collapseToggle = () => {
    setcollapsed(!collapsed);
  };

  const getWorkSpaceDetails = async () => {
    try {
      const localaccessToken = await getAccessTokenSilently({
        audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
        scope: "read:current_user",
      });

      const userWorkSpaceReq = await request(`http://localhost:5000/workspaces/12`, {
        method: "get",
        headers: {
          Authorization: `Bearer ${localaccessToken}`,
          email: `${user.email}`,
        },
      });
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
  return (
    <Layout className="main_container">
      <Header className="header">
        <Navbar activePage="2" />
      </Header>
      <Layout>
        <Content style={{margin: "50px", padding: "20px"}}>
          <Card style={{minHeight: "60vh"}}>
            <Preferences />
            <Button
              type="primary"
              style={{float: "right", marginRight: "7em", minWidth: "11vw", marginTop: "10px"}}
              onClick={() => {
                settrained(true);
              }}
            >
              {trained ? "Retrain Model" : "Train Model"}
            </Button>
          </Card>
        </Content>
      </Layout>
      <Footer></Footer>
    </Layout>
  );
}

export default Trainer;
