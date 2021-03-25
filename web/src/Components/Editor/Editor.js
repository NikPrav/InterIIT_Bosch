import react, {useState, useEffect} from "react";
import "antd/dist/antd.css";
import {Layout, Menu, Empty, Card, Dropdown, Button, Switch, Slider, Typography, Modal} from "antd";
import {DesktopOutlined, FolderAddFilled} from "@ant-design/icons";
import {IoSettingsSharp} from "react-icons/io5";
import "./styles.css";
import Navbar from "./../Navbar/Navbar";
import ImageRow from "../ImageRow/ImageRow";
import img from "./../PopupImage/stop.png";
import Checkbox from "antd/lib/checkbox/Checkbox";
import {useAuth0} from "@auth0/auth0-react";
import request from "umi-request";
import {useParams} from "react-router";

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
  const [AugType, setAugType] = useState("User Selected Images");
  const Augmenu = (
    <Menu>
      <Menu.Item
        onClick={() => {
          setAugType("User Selected Images");
        }}
      >
        User Selected Images
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setAugType("Randomly Applied");
        }}
      >
        Randomly Applied
      </Menu.Item>
      <Menu.Item
        onClick={() => {
          setAugType("Bulk Augmentation");
        }}
      >
        Bulk Augmentation
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
          <strong>Augmentation Preferences</strong>

          <Dropdown trigger={["click"]} overlay={Augmenu}>
            <Button style={{float: "right", minWidth: "10vw"}}>{AugType}</Button>
          </Dropdown>
        </p>
      </div>
    </Card>
  );
}

function Editor(props) {
	const wid = (parseInt(props.location.search.substr(14), 10));
  const [workspaceDetails, setWorkspaceDetails] = useState({});
  const {user, isAuthenticated, getAccessTokenSilently} = useAuth0();
  const {Header, Footer, Sider, Content} = Layout;
  const [collapsed, setcollapsed] = useState(false);
  const [selectedSection, setselectedSection] = useState(0);
  const collapseToggle = () => {
    setcollapsed(!collapsed);
  };

  const [isDatasetModalVisible, setisDatasetModalVisible] = useState(false);
  const showDatasetModal = () => {
    setisDatasetModalVisible(true);
  };

  const handleOk = () => {
    setisDatasetModalVisible(false);
    console.log("Okayed");
  };

  const handleCancel = () => {
    setisDatasetModalVisible(false);
    console.log("Cancelled");
  };
  const onCheckboxChange = checkedValues => {
    console.log("checked = ", checkedValues);
  };

  const getWorkSpaceDetails = async () => {
    try {
      const localaccessToken = await getAccessTokenSilently({
        audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
        scope: "read:current_user",
      });

      const userWorkSpaceReq = await request(`${process.env.REACT_APP_API_URL}/workspaces/${wid}`, {
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
      <Navbar activePage="1" />
      <Layout>
        <Sider collapsible collapsed={collapsed} theme="light" onCollapse={collapseToggle}>
          <Menu theme="light" mode="inline">
            <Menu.Item
              key="0"
              icon={<FolderAddFilled />}
              onClick={() => {
                setselectedSection(0);
                showDatasetModal();
              }}
            >
              {" "}
              Manage DataSets
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
          </Menu>
        </Sider>

        <Modal
          title="Manage Datasets"
          visible={isDatasetModalVisible}
          onOk={handleOk}
          onCancel={handleCancel}
          footer={[
            <Button
              type="primary"
              onClick={handleCancel}
              style={{paddingRight: "5px", paddingLeft: "5px", marginRight: "5px"}}
            >
              Cancel
            </Button>,
            <Button
              key="edit"
              type="primary"
              onClick={handleOk}
              style={{paddingRight: "5px", paddingLeft: "5px", marginRight: "5px"}}
            >
              Continue
            </Button>,
          ]}
        >
          <p>The Following Datasets are currently being used in this workspace</p>
          Choose to continue/add more datasets below. Note: Removing a Dataset will also remove it's
          related Augmentations.{" "}
          {/* <Dropdown overlay={menu}>
              <Button style={{minWidth: "30px"}}>{buttonState}</Button>
            </Dropdown> */}
          <div>
            <Checkbox>German Dataset</Checkbox>
          </div>
          <div>
            <Checkbox>Indian Dataset</Checkbox>
          </div>
          <div>
            <Checkbox>British Dataset</Checkbox>
          </div>
          {/*<Checkbox.Group options={options} onChange={onCheckboxChange} defaultValue={['GermanDataset']} />*/}
        </Modal>

        <Content style={{marginTop: "40px", marginLeft: "10px"}}>
          <Card style={{minHeight: "100vh"}}>
            {selectedSection ? <Preferences /> : <ImageRow DataClass="Stop Sign" />}
            {/* {selectedSection ? <Preferences /> : <ImageRow DataClass="Stop Sign" />} */}
          </Card>
        </Content>
      </Layout>
      <Footer></Footer>
    </Layout>
  );
}

export default Editor;
