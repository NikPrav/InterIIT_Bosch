import react from "react";
import {Button, PageHeader, Typography} from "antd";
import Layout, {Content, Footer, Header} from "antd/lib/layout/layout";
import {FontColorsOutlined} from "@ant-design/icons";
import "./styles.css";
// import Title from "antd/lib/skeleton/Title";
const {Title} = Typography;
// const { Header, Content, Footer } = Layout;

function Landing() {
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
          <Button type="primary" href="/editor" size="large">
            Login
          </Button>
          <div style={{textAlign: "center"}}>
            Press button to login, and add more text to make it look cool
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

export default Landing;
