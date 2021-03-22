import react, {useState} from "react";
import {Typography, List, Button, Layout, Modal, Card, Space, Dropdown, Menu} from "antd";
import "./styles.css";
import {Content} from "antd/lib/layout/layout";
import Navbar from "../Navbar/Navbar";
import { useAuth0 } from "@auth0/auth0-react";


function Home() {
  const {Title, Paragraph, Text, Link} = Typography;
  const [buttonState, setButtonState] = useState("German DataSet");
  // const user = {name: "Rachit"};
  const { user, isAuthenticated, isLoading } = useAuth0();

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

  const [isModalVisible, setisModalVisible] = useState(false);
  const showModal = () => {
    setisModalVisible(true);
  };

  const handleOk = () => {
    setisModalVisible(false);
  };

  const handleCancel = () => {
    setisModalVisible(false);
  };
  return (
    isAuthenticated &&(
    <Layout>
      <Navbar />
      <Layout.Content className="home-content">
        <div className="home-heading" >
          <div style={{textAlign:"center"}}>
          <Title>Welcome, {user.name.split(' ')[0]} !</Title>
          <Text strong>Here are your existing workspaces:</Text>
          <Button onClick={showModal} type="primary" style={{marginLeft: "5px"}}>
            Create New
          </Button>
          </div>
          <Modal
            title="New Workspace"
            visible={isModalVisible}
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
                key="train"
                href="/editor"
                type="primary"
                style={{paddingRight: "5px", paddingLeft: "5px", marginRight: "5px"}}
              >
                Train
              </Button>,
              <Button
                key="edit"
                href="/editor"
                type="primary"
                style={{paddingRight: "5px", paddingLeft: "5px", marginRight: "5px"}}
              >
                Edit Dataset
              </Button>,
            ]}
          >
            <p>
              Choose a dataset from the dropdown and hint train to get quickly started or manually
              fine-tune your dataset.
            </p>
            Choose a dataset below to get started:{" "}
            <Dropdown overlay={menu}>
              <Button>{buttonState}</Button>
            </Dropdown>
          </Modal>

          <div class="list-container">
            <List bordered className="home-list" size="large">
              <List.Item>
                <Text>1.</Text>Default Workspace
                <Button type="primary" style={{float: "right"}} className="button" href="/editor">
                  Edit
                </Button>
                <Button type="primary" style={{float: "right"}} className="button" href="/editor">
                  Test
                </Button>
              </List.Item>
              <List.Item>
                <Text>2.</Text>Yet Another Workspace
                <Button type="primary" style={{float: "right"}} className="button" href="/editor">
                  Edit
                </Button>
                <Button type="primary" style={{float: "right"}} className="button" href="/editor">
                  Test
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
