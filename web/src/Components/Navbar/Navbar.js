import {Layout, Menu, Avatar, Button, Steps} from "antd";
import React from "react";

function Navbar(props) {
  const {Step} = Steps;
  const {activePage} = props;
  return (
    <Layout.Header>
      <div className="logo"></div>
      <Menu theme="dark" mode="horizontal" selectedKeys={activePage}>
        <Menu.Item key="1" onClick="/editor">
          <a href="/editor">Dataset</a>
        </Menu.Item>
        <Menu.Item key="2" onClick="/trainer">
          <a href="/trainer">Training</a>
        </Menu.Item>
        <Menu.Item key="3">Inference</Menu.Item>
        <Avatar style={{float: "right", marginTop: "15px", marginLeft: "25px"}}>R</Avatar>
        <Button style={{float: "right", paddingLeft: "10px", marginTop: "15px"}}>Sign out</Button>
      </Menu>
    </Layout.Header>
  );
}

export default Navbar;
