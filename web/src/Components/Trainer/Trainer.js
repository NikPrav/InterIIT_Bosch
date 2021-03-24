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
  const [buttonState, setButtonState] = useState("CategoricalCrossEntropy");
  const [optimizerfn, setoptimizerfn] = useState("Sgd");
  const LossFns = ["CategoricalCrossEntropy", "MeanSquaredError"];

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
          setoptimizerfn("Sgd");
        }}
      >
        Sgd
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setoptimizerfn("Momentum");
        }}
      >
        Momentum
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setoptimizerfn("Adagrad");
        }}
      >
        Adagrad
      </Menu.Item>
      <Menu.Item
        danger
        onClick={() => {
          setoptimizerfn("Rmsprop");
        }}
      >
        Rmsprop
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
          <Typography.Text>Epochs</Typography.Text> <PrefSlider min={1} max={20} step={1} />
        </p>
        <p>
          <Typography.Text>Learning Rate</Typography.Text> <PrefSlider min={0} max={1} step={0.1} />
        </p>
        <p>
          <Typography.Text>Test-Train Split</Typography.Text>{" "}
          <PrefSlider min={0} max={1} step={0.1} />
        </p>
        <p>
          Loss Function
          <Dropdown trigger={["click"]} overlay={LossFnDropdown}>
            <Button style={{float: "right", minWidth: "10vw"}}>{buttonState}</Button>
          </Dropdown>
        </p>
        <p>
          Optimizer Function
          <Dropdown trigger={["click"]} overlay={OptimizerDropdown}>
            <Button style={{float: "right", minWidth: "10vw"}}>{optimizerfn}</Button>
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
        {/* <Sider collapsible collapsed={collapsed} theme="light" onCollapse={collapseToggle}>
          <Menu theme="light" mode="inline">
            <Menu.Item
              key="0"
              icon={<FolderAddFilled />}
              onClick={() => {
                setselectedSection(0);
              }}
            >
              
              Import
            </Menu.Item>
            <Menu.Item
              key="1"
              icon={<IoSettingsSharp />}
              onClick={() => {
                setselectedSection(1);
              }}
            >
              {" "}
              Settings
            </Menu.Item>
            <Menu.Item key="3" icon={<GoGraph />}>
              {" "}
              Graph
            </Menu.Item>
          </Menu>
        </Sider> */}
        <Content style={{margin: "50px", padding: "20px"}}>
          <Card style={{minHeight: "60vh"}}>
            <Preferences />
            <Button type="primary" style={{float: "right", marginRight: "7em"}}>
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
