import react, {useState, useEffect} from "react";
import {Typography, List, Button, Layout, Modal, Card, Space, Dropdown, Menu} from "antd";
import "./styles.css";
import {Content} from "antd/lib/layout/layout";
import Navbar from "../Navbar/Navbar";
import Checkbox from "antd/lib/checkbox/Checkbox";
import {useAuth0} from "@auth0/auth0-react";
import request, {extend} from "umi-request";

const {confirm} = Modal;

function Home() {
  const {Title, Paragraph, Text, Link} = Typography;
  const [buttonState, setButtonState] = useState("German DataSet");
  const {user, isAuthenticated, getAccessTokenSilently} = useAuth0();
  const [accessToken, setAccessToken] = useState(null);
  const [workspaceList, setworkspaceList] = useState([]);

  const loginApi = async () => {
    const getUserMetadata = async () => {
      // console.log(user)
      const domain = "dev-kqx4v2yr.jp.auth0.com";
      try {
        const localaccessToken = await getAccessTokenSilently({
          audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
          scope: "read:current_user",
        });
        const UrlToSendDataTo = `http://localhost:5000/register`;

        setAccessToken(localaccessToken);
        const CallUmiApi = await request(UrlToSendDataTo, {
          method: "post",
          headers: {
            Authorization: `Bearer ${localaccessToken}`,
            email: `${user.email}`,
          },
        });
        const umimessage = await CallUmiApi;
        console.log(umimessage);
      } catch (e) {
        console.log(`Error:${e.message}`);
      }
    };
    getUserMetadata();
  };

  const getWorkSpaces = async () => {
    try {
      const localaccessToken = await getAccessTokenSilently({
        audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
        scope: "read:current_user",
      });

      const userWorkSpaceReq = await request("http://localhost:5000/workspaces", {
        method: "get",
        headers: {
          Authorization: `Bearer ${localaccessToken}`,
          email: `${user.email}`,
        },
      });

      const umimessage = await userWorkSpaceReq;
      setworkspaceList(umimessage);
      console.log(umimessage);
    } catch (e) {
      console.log(e.message);
    }
  };

  useEffect(
    async user => {
      console.log("Calling API");
      await loginApi();
      await getWorkSpaces();
    },
    [user]
  );

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

  const createWorkSpaceApi = async () => {
    try {
      const localaccessToken = await getAccessTokenSilently({
        audience: `https://dev-kqx4v2yr.jp.auth0.com/api/v2/`,
        scope: "read:current_user",
      });

      const userWorkSpaceCreate = await request("http://localhost:5000/workspaces", {
        method: "post",
        headers: {
          Authorization: `Bearer ${localaccessToken}`,
          email: `${user.email}`,
        },
        data: {
          name: "Why does this need a name?",
        },
      });
      console.log("Create Workspace Sent");
      const umimessage = await userWorkSpaceCreate;
      setworkspaceList([...workspaceList, umimessage]);
      console.log(umimessage);
      console.log("WorkSpace List");
      console.log(workspaceList);
    } catch (e) {
      console.log(e.message);
    }
  };

  const handleOk = async () => {
    await createWorkSpaceApi();
    await getWorkSpaces();
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
        <Navbar isOutside />
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
                  onClick={handleOk}
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
                    href="/editor?workspace_id={}"
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
                {workspaceList.map(inst => (
                  <List.Item>
                    <Text>2.</Text>
                    {inst.name}
                    <Button
                      type="primary"
                      style={{float: "right"}}
                      className="button"
                      href="/editor"
                    >
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
                ))}
                <List.Item>
                  <Button
                    type="primary"
                    style={{float: "right", alignSelf: "flex-end"}}
                    onClick={showWorkspaceModal}
                  >
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
