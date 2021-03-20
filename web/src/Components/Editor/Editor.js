import react, {useState} from "react";
import "antd/dist/antd.css";
import {Layout, Menu, Empty} from "antd";
import {
  DesktopOutlined,
  PieChartOutlined,
  FileFilled,
  FolderAddFilled,
  TeamOutlined,
} from "@ant-design/icons";
import "./styles.css";
import Navbar from "./../Navbar/Navbar";

function Editor() {
  const {Header, Footer, Sider, Content} = Layout;
  const [collapsed, setcollapsed] = useState(false);

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
            <Menu.Item key="1" icon={<FolderAddFilled />}>
              {" "}
              Dataset
            </Menu.Item>
            {/*
            <Menu.Item key="2" icon={<FileFilled />}>
              {" "}
              Add a Layer
            </Menu.Item>*/}
            <Menu.Item key="3" icon={<DesktopOutlined />}>
              {" "}
              Outline
            </Menu.Item>

            <Menu.Item key="4" icon={<TeamOutlined />}>
              {" "}
              HyperParameters
            </Menu.Item>

            <Menu.Item key="5" icon={<DesktopOutlined />}>
              {" "}
              Optimizer
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
          <Empty />
        </Content>
      </Layout>
      <Footer></Footer>
    </Layout>
  );
}

export default Editor;
