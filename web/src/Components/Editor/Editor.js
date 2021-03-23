import react, {useState} from "react";
import "antd/dist/antd.css";
import {Layout, Menu, Empty, Card, Dropdown, Button, Switch, Slider, Typography} from "antd";
import {DesktopOutlined, FolderAddFilled} from "@ant-design/icons";
import {IoSettingsSharp} from "react-icons/io5";
import "./styles.css";
import Navbar from "./../Navbar/Navbar";
import ImageRow from "../ImageRow/ImageRow";
import img from "./../PopupImage/stop.png";

function PrefSlider(props) {
  const {max, min, step} = props;
  const [sliderValue, setSliderValue] = useState(min);
  const handleChange = val => {
    setSliderValue(val);
  };
  return (
    <div style={{maxWidth: "600px", float: "right", width: "31vw"}}>
      <Slider min={min} max={max} step={step} value={sliderValue} onChange={handleChange} />
    </div>
  );
}

function Preferences() {
  const [buttonState, setButtonState] = useState("German DataSets");
  const LossFns = ["CategoricalCrossEntropy", "MeanSquaredError"];

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
      <Navbar activePage="1" />
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
        <Content style={{marginTop: "40px", marginLeft: "10px"}}>
          <Card style={{minHeight: "100vh"}}>
            {selectedSection ? <Preferences /> : <ImageRow />}
          </Card>
        </Content>
      </Layout>
      <Footer></Footer>
    </Layout>
  );
}

export default Editor;
