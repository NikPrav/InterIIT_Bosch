import {Layout, Menu, Avatar, Button, Steps} from "antd";
import React from "react";
import {useAuth0} from "@auth0/auth0-react";

function Navbar(props) {
  const {Step} = Steps;
  const {activePage} = props;

  const {logout} = useAuth0();
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
        <Menu.Item key="3">
          <a href="/infer">Inference</a>
        </Menu.Item>
        <Avatar style={{float: "right", marginTop: "15px", marginLeft: "25px"}}>R</Avatar>
        <Button
          type="danger"
          style={{float: "right", paddingLeft: "10px", marginTop: "15px"}}
          onClick={() => logout({returnTo: window.location.origin})}
        >
          Sign out
        </Button>
      </Menu>
    </Layout.Header>
  );
}

export default Navbar;
