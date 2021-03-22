import {Layout, Menu, Avatar, Button} from "antd";
import React from "react";

function Navbar(props) {
  const {activePage} = props;
  return (
    <Layout.Header>
      <div className="logo"></div>
      <Menu theme="dark" mode="horizontal" selectedKeys={activePage}>
        <Menu.Item key="1">Dataset</Menu.Item>
        <Menu.Item key="2">Training</Menu.Item>
        <Menu.Item key="3">Inference</Menu.Item>
        <Avatar style={{float: "right", marginTop: "15px", marginLeft: "25px"}}>R</Avatar>
        <Button style={{float: "right", paddingLeft: "10px", marginTop: "15px"}}>Sign out</Button>
      </Menu>
    </Layout.Header>
  );
}

export default Navbar;
