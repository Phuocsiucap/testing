import Laptop from "./Laptop";
import Ultrabook from "./Ultrabook";
import PhuKien from "./PhuKien";
import { useEffect, useState } from "react";
import { request1 } from "../../../utils/request";
import { isArray } from "chart.js/helpers";

// Loading Spinner Component
const LoadingSpinner = () => (
  <div className="flex justify-center items-center min-h-[400px]">
    <div className="flex flex-col items-center">
      <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary"></div>
      <p className="mt-4 text-gray-600 font-medium">Đang tải sản phẩm...</p>
    </div>
  </div>
);

function Content() {
  const [good, setGood] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetch = async () => {
      try {
        setLoading(true);
        const response = await request1.get("goods/list");
        const data = response.data;
        setGood(data);
      } catch (e) {
        console.log("Có lỗi ", e);
      } finally {
        setLoading(false);
      }
    };
    fetch();
  }, []);

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div>
      <Laptop good={good} />
      <Ultrabook good={good} />
      <PhuKien good={good} />
    </div>
  );
}

export default Content;
