import React, {useState} from "react";
import Navbar from "../Navbar/Navbar";
import {Layout, Header, Dropdown, Button, Typography, Menu, Card, Slider} from "antd";
import {DesktopOutlined, FolderAddFilled} from "@ant-design/icons";
import {IoSettingsSharp} from "react-icons/io5";

function PrefSlider(props) {
  const {max, min, step} = props;
  const [sliderValue, setSliderValue] = useState(min);
  const handleChange = val => {
    setSliderValue(val);
  };
  return (
    <div style={{maxWidth: "600px", float: "right", width: "600px"}}>
      <Slider min={min} max={max} step={step} value={sliderValue} onChange={handleChange} />
    </div>
  );
}

function Preferences() {
  const [buttonState, setButtonState] = useState("German DataSets");
  const LossFns = ["CategoricalCrossEntropy", "MeanSquaredError"];
  
  const Simple = (item) => {
    <Menu.Item>
        {item}
    </Menu.Item>
  };
  const LossFnDropdown = (
    <Menu>
      <Menu.Item
        onClick={() => {
          setButtonState("German DataSet");
        }}
      >
        German DataSet
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setButtonState("British DataSet");
        }}
      >
        British DataSet
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setButtonState("Indian DataSet");
        }}
      >
        Indian DataSet
      </Menu.Item>
      <Menu.Item
        danger
        onClick={() => {
          setButtonState("Blank DataSet");
        }}
      >
        Blank DataSet
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
          Loss Function
          <Dropdown trigger={['click']} overlay={
              <Menu>
                  {
                  LossFns.map((func)=>{
                    <Menu.Item>
                        Hello {func}
                    </Menu.Item>
                  })
                  }
              </Menu>
          }>
            <Button style={{float: "right"}}>{buttonState}</Button>
          </Dropdown>
        </p>
        <p>
          Optimizer Function
          <Dropdown trigger={['click']} overlay={LossFnDropdown}>
            <Button style={{float: "right"}}>{buttonState}</Button>
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
        <Sider collapsible collapsed={collapsed} theme="light" onCollapse={collapseToggle}>
          <Menu theme="light" mode="inline">
            <Menu.Item
              key="0"
              icon={<FolderAddFilled />}
              onClick={() => {
                setselectedSection(0);
              }}
            >
              {" "}
              Import
            </Menu.Item>
            {/*
             */}
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
            <Menu.Item key="6" icon={<DesktopOutlined />}>
              {" "}
              Augmentation
            </Menu.Item>

            <Menu.Item key="7" icon={<DesktopOutlined />}>
              {" "}
              Graph
            </Menu.Item>
          </Menu>
        </Sider>
        <Content>
          <Preferences />
        </Content>
      </Layout>
      <Footer></Footer>
    </Layout>
  );
}

export default Trainer;
