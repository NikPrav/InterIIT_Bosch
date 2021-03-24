import React from "react";
import {Layout, Typography} from "antd";
import Navbar from "../Navbar/Navbar";

function Infer() {
  const {Title, Text, Link} = Typography;
  return (
    <Layout>
      <Navbar activePage="3" />
      <Layout.Content style={{padding: "20px 20px 20px 20px"}}>
        <Title>Criterion 1</Title>
      </Layout.Content>
    </Layout>
  );
}

export default Infer;
