import react from "react";
import {Typography, List, Button, Space, Layout} from "antd";
import "./styles.css";
import {Content} from "antd/lib/layout/layout";
import Navbar from "../Navbar/Navbar";

function Home() {
  const {Title, Paragraph, Text, Link} = Typography;
  const user = {name: "Rachit"};
  return (
    <Layout>
      <Navbar />
      <Layout.Content className="home-content">
        <div className="home-heading">
          <Title>Welcome, {user.name} !</Title>
          <Text strong>Here are your existing workspaces:</Text>
          <div class="list-container">
            <List bordered className="home-list" size="large">
              <List.Item>
                <Text mark>1.</Text>Default Workspace
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
  );
}

export default Home;
