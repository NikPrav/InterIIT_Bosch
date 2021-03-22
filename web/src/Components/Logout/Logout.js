import react from "react";
import {Button, PageHeader, Typography} from "antd";
import Layout, {Content, Footer, Header} from "antd/lib/layout/layout";
import {FontColorsOutlined} from "@ant-design/icons";
import "./styles.css";
// import Title from "antd/lib/skeleton/Title";
const {Title} = Typography;
// const { Header, Content, Footer } = Layout;

function Logout() {
  return (
    <Layout className="fullpage">
      {/* <PageHeader className = 'site-page-header' title = 'InterIIT Bosch Traffic Sign Detector' textAlign='center'>

            </PageHeader> */}
      <Header classname="site-leayout-subheader-background">
        <Title level={2} style={{color: "white", padding: "10px"}}>
          InterIIT Bosch Traffic Sign Recogniser
        </Title>
      </Header>

      <Content className="site-layout-content">
        <div class="center">
          <div style={{textAlign: "center"}}>
            You've succesfully logged out hehe
          </div>
        </div>
      </Content>

      <Footer className="site-layout-footer">
        <div>
          <a style={{float: "left"}} href="https://github.com/npalladium/InterIIT-Bosch">
            Github link
          </a>
          <b style={{float: "right"}}>IIT Hyderabad,2021</b>
        </div>
      </Footer>
    </Layout>
  );
}

export default Logout;