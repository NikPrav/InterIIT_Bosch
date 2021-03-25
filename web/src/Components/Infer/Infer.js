import React from "react";
import {Layout, Typography, Image, Card} from "antd";
import Navbar from "../Navbar/Navbar";
import result from "./index_image.jpeg";

function Infer() {
  const {Title, Text, Link} = Typography;
  return (
    <Layout>
      <Navbar activePage="3" />
      <Layout.Content style={{margin: "60px"}}>
        <Card style={{minHeight: "50vh"}}>
          <div>
            <Title>Criterion 1</Title>
            <div style={{display: "flex", justifyContent: "space-between", marginLeft: "5vw"}}>
              <Image src={result} width="30vw" />
              <Card style={{marginRight: "15vw"}} title="Saliency Map">
                This is a two-line description that will be provided by the backend
                <br />
                Second Line of Description
              </Card>
            </div>
          </div>
        </Card>
      </Layout.Content>
    </Layout>
  );
}

export default Infer;
