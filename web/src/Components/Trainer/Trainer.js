import React, {useState} from "react";
import Navbar from "../Navbar/Navbar";
import {Layout, Header, Dropdown, Button, Typography, Menu, Card, Slider} from "antd";
import {DesktopOutlined, FolderAddFilled} from "@ant-design/icons";
import {IoSettingsSharp} from "react-icons/io5";
import {GoGraph} from "react-icons/go";

function PrefSlider(props) {
  const {max, min, step} = props;
  const [sliderValue, setSliderValue] = useState(min);
  const handleChange = val => {
    setSliderValue(val);
  };
  return (
    <div style={{maxWidth: "32vw", float: "right", width: "600px"}}>
      <Slider min={min} max={max} step={step} value={sliderValue} onChange={handleChange} />
    </div>
  );
}

function Preferences() {
  const [buttonState, setButtonState] = useState("nll_lossfunction");
  const [optimizerfn, setoptimizerfn] = useState("Sgd");
  //const LossFns = ["CategoricalCrossEntropy", "MeanSquaredError"];

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
          <Typography.Text>Batch Size:</Typography.Text> <PrefSlider min={1} max={20} step={1} />
        </p>
        <p>
          <Typography.Text>Epochs</Typography.Text> <PrefSlider min={1} max={2000} step={100} />
        </p>
        <p>
          <Typography.Text>Learning Rate</Typography.Text> <PrefSlider min={0} max={5} step={0.2} />
        </p>
        <p>
          <Typography.Text>Test-Train Split</Typography.Text>{" "}
          <PrefSlider min={0} max={1} step={0.1} />
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
  const {Header, Footer, Sider, Content} = Layout;
  const [collapsed, setcollapsed] = useState(false);
  const [selectedSection, setselectedSection] = useState(0);
  const collapseToggle = () => {
    setcollapsed(!collapsed);
  };
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
            >
              Train Model
            </Button>
          </Card>
        </Content>
      </Layout>
      <Footer></Footer>
    </Layout>
  );
}

export default Trainer;
