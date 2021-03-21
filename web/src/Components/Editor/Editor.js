import react, {useState} from "react";
import "antd/dist/antd.css";
import {Layout, Menu, Empty, Card, Dropdown, Button, Switch, Slider, Typography} from "antd";
import {DesktopOutlined, FolderAddFilled, TeamOutlined} from "@ant-design/icons";
import {IoSettings, IoSettingsSharp} from "react-icons/io5";
import "./styles.css";
import Navbar from "./../Navbar/Navbar";
import PopupImage from "../PopupImage/PopupImage";
import ImageRow from "../ImageRow/ImageRow";

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
          <strong>Viewer Preferences</strong>
        </p>
        <p>
          Show Augmentated Images in DataSet Viewer:{" "}
          <Switch defaultChecked style={{float: "right"}} />
        </p>

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
          <Dropdown overlay={LossFnDropdown}>
            <Button style={{float: "right"}}>{buttonState}</Button>
          </Dropdown>
        </p>
        <p>
          Optimizer Function
          <Dropdown overlay={LossFnDropdown}>
            <Button style={{float: "right"}}>{buttonState}</Button>
          </Dropdown>
        </p>
      </div>
    </Card>
  );
}

function Editor() {
  const {Header, Footer, Sider, Content} = Layout;
  const [collapsed, setcollapsed] = useState(false);
  const [selectedSection, setselectedSection] = useState(0);
  const collapseToggle = () => {
    setcollapsed(!collapsed);
  };
  return (
    <Layout className="main_container">
      <Header className="header">
        <Navbar />
      </Header>
      <Layout>
        <Sider collapsible collapsed={collapsed} onCollapse={collapseToggle}>
          <Menu theme="dark" mode="inline">
            <Menu.Item
              key="0"
              icon={<FolderAddFilled />}
              onClick={() => {
                setselectedSection(0);
              }}
            >
              {" "}
              Dataset
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
              Evaluate
            </Menu.Item>

            <Menu.Item key="7" icon={<DesktopOutlined />}>
              {" "}
              Graph
            </Menu.Item>
          </Menu>
        </Sider>
        <Content>
          {selectedSection ? <Preferences /> : <ImageRow />}
          <div style={{display: "none"}}>
            <ImageRow />
            <Empty />
          </div>
        </Content>
      </Layout>
      <Footer></Footer>
    </Layout>
  );
}

export default Editor;
