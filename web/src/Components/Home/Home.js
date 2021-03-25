import react, {useState,useEffect} from "react";
import {Typography, List, Button, Layout, Modal, Card, Space, Dropdown, Menu} from "antd";
import "./styles.css";
import {Content} from "antd/lib/layout/layout";
import Navbar from "../Navbar/Navbar";
import Checkbox from "antd/lib/checkbox/Checkbox";
import {useAuth0} from "@auth0/auth0-react";

const {confirm} = Modal;

function Home() {
  const {Title, Paragraph, Text, Link} = Typography;
  const [buttonState, setButtonState] = useState("German DataSet");
  // const user = {name: "Rachit"};
  const {user, isAuthenticated, getAccessTokenSilently} = useAuth0();
  // const [userMetadata, setUserMetadata] = useState(null);
  // getUserMetadata();

  const callApi = async () => { 
    const getUserMetadata = async () => {

      // console.log(user)
      const domain = "dev-kqx4v2yr.jp.auth0.com";
  
      try {
        const accessToken = await getAccessTokenSilently({
          audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
          scope: "read:current_user",
        });
        const UrlToSendDataTo = `http://localhost:5000/test`;
        ;

        const CallPrivateApi = await fetch(UrlToSendDataTo, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            User_sub:`${user.sub}`,
          },
        });
        const  message  = await CallPrivateApi.json();
        console.log(message)
      } catch (e) {
        console.log(`Error:${e.message}`);
      }
    };
  
    getUserMetadata();
  };
  useEffect((user) =>  {  
    console.log('Calling API')  
    callApi();  
  },[user]);

  const menu = (
    <Menu>
      <Menu.Item>
        <a
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => {
            setButtonState("German DataSet");
          }}
        >
          German DataSet
        </a>
      </Menu.Item>
      <Menu.Item>
        <a
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => {
            setButtonState("British DataSet");
          }}
        >
          British DataSet
        </a>
      </Menu.Item>
      <Menu.Item>
        <a
          target="_blank"
          rel="noopener noreferrer"
          onClick={() => {
            setButtonState("Indian DataSet");
          }}
        >
          Indian DataSet
        </a>
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

  const [isWorkspaceModalVisible, setisWorkspaceModalVisible] = useState(false);
  const showWorkspaceModal = () => {
    setisWorkspaceModalVisible(true);
  };

  const handleOk = () => {
    setisWorkspaceModalVisible(false);
  };

  const handleCancel = () => {
    setisWorkspaceModalVisible(false);
  };
  const options = [
    {label: "GermanDataset", value: "GermanDataset"},
    {label: "IndianDataset", value: "IndianDataset"},
    {label: "BritishDataset", value: "BritishDataset"},
  ];
  const defaultOptions = ["German DataSet"];
  const onCheckboxChange = checkedValues => {
    console.log("checked = ", checkedValues);
  };

  function showDeleteConfirm() {
    confirm({
      title: "Are you sure delete this Workspace?",
      // icon: <ExclamationCircleOutlined />,
      content: "This action is permanent and all associated images will be lost ",
      okText: "Yes",
      okType: "danger",
      cancelText: "No",
      onOk() {
        console.log("OK");
        // return new Promise((resolve, reject) => {
        //   setTimeout(Math.random() > 0.5 ? resolve : reject, 1000);
        // }).catch(() => console.log('Oops errors!'));
      },
      onCancel() {
        console.log("Cancel");
      },
    });
  }

  return (
    isAuthenticated && (
      <Layout>
        <Navbar />
        <Layout.Content className="home-content">
          <div className="home-heading">
            <div style={{textAlign: "center"}}>
              <Title>Welcome, {user.name} !</Title>
              <Text strong>Here are your existing workspaces:</Text>
            </div>
            <Modal
              title="New Workspace"
              visible={isWorkspaceModalVisible}
              onOk={handleOk}
              onCancel={handleCancel}
              footer={[
                <Button
                  type="danger"
                  onClick={handleCancel}
                  style={{paddingRight: "5px", paddingLeft: "5px", marginRight: "5px"}}
                >
                  Cancel
                </Button>,
                <Button
                  key="edit"
                  href="/editor"
                  type="primary"
                  style={{paddingRight: "5px", paddingLeft: "5px", marginRight: "5px"}}
                >
                  Create
                </Button>,
              ]}
            >
              <p>
                Choose a dataset from below to get started. You can add images manually later to
                fine-tune your dataset.
              </p>
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

            <div class="list-container">
              <List bordered className="home-list" size="large">
                <List.Item>
                  <Text>1.</Text>Default Workspace
                  <Button type="primary" style={{float: "right"}} className="button" href="/editor">
                    Use
                  </Button>
                  <Button
                    type="danger"
                    disabled
                    style={{float: "right"}}
                    className="button"
                    href="/editor"
                  >
                    Delete
                  </Button>
                </List.Item>
                <List.Item>
                  <Text>2.</Text>Yet Another Workspace
                  <Button type="primary" style={{float: "right"}} className="button" href="/editor">
                    Use
                  </Button>
                  <Button
                    type="danger"
                    style={{float: "right"}}
                    className="button"
                    // href="/editor"
                    onClick={showDeleteConfirm}
                  >
                    Delete
                  </Button>
                </List.Item>
                <List.Item>
                  <Button
                    type="primary"
                    style={{float: "right", alignSelf: "flex-end"}}
                    onClick={showWorkspaceModal}
                  >
                    {" "}
                    CREATE NEW
                  </Button>
                </List.Item>
              </List>
            </div>
          </div>
        </Layout.Content>
      </Layout>
    )
  );
}

export default Home;
