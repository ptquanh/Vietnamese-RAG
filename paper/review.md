# Review bản thảo ngày 15/10/2026

Bản thảo đã được bổ sung nền tảng contrastive loss và rà soát nội dung, công thức, dữ liệu, nguồn kết quả và dàn trang. Phần trình bày có thể tiếp tục chỉnh để nộp, nhưng bằng chứng hiện có chưa đủ để khẳng định H-SupCon cải thiện NER nhất quán hoặc vượt baseline. Không chạy lại huấn luyện hay đánh giá từ dự đoán gốc trong lần review này.

## Các vấn đề còn mở, theo mức độ ưu tiên

### 1. Cần bổ sung log nguồn cho hai hàng kết quả

**Mức độ: cao.** PhoBERT V2 + CRF (98,75/97,22/97,98) và ELECTRA + CRF-H-SupCon (98,20/98,60/98,40) hiện chỉ có trong bảng tổng hợp của main.tex; chưa tìm thấy log nguồn tương ứng trong các thư mục đã khảo sát. Nhận xét tăng SL 0,15 điểm và giảm F1 tổng thể 0,06 điểm đều dựa một phần vào hàng baseline này nên còn tạm thời. Các bảng đã đánh dấu hai hàng bằng ký hiệu †, và abstract/kết luận chỉ nêu các kết quả có log. Cần log test, định danh checkpoint, cấu hình, mã băm test và dự đoán gốc trước khi coi những so sánh này là kết quả đã kiểm chứng.

### 2. Chưa xác nhận giao thức BIO và chế độ strict của bộ đánh giá

**Mức độ: cao.** Có thể tính lại Micro P/R/F1 khớp biên và loại từ tổng số đếm trong ba log. Tuy nhiên, điều này không chứng minh đã dùng `seqeval` với `mode="strict", scheme=IOB2`. Tệp test cục bộ có 20.977 nhãn B-X, còn hai log test 10.278 mẫu ghi 20.979 thực thể vàng. Bộ đánh giá CoNLL trong repo PhoBERT-Legal-NER có cách diễn giải I-X không có B-X hợp lệ; đó là một nguyên nhân có thể có, chưa được xác nhận là evaluator đã tạo các log này. Cần xuất dự đoán, giữ ranh giới câu và chạy cùng một evaluator với phiên bản, scheme và quy tắc BIO cố định. Không trộn F1 theo nhãn token, F1 theo thực thể và chế độ strict/IOB2.

### 3. Tính tái lập của cấu hình huấn luyện chưa đầy đủ

**Mức độ: cao.** Bảng cấu hình hiện được xác định rõ là thông tin từ tài liệu thiết kế, chưa phải bằng chứng đã quét siêu tham số hay áp dụng đồng nhất cho mọi run. Các log ngày 14/10 chỉ ghi đường dẫn checkpoint và kết quả test. Chưa đủ thông tin để xác nhận model/tokenizer ID và revision, seed, batch hiệu dụng, xử lý subword và token đặc biệt, chiều dài chuỗi, số mẫu bị cắt, CRF reduction, kích thước đầu chiếu và lịch chọn checkpoint. Đặc biệt cần đối chiếu code H-SupCon thực thi với công thức, cách loại O, tự so sánh và anchor không có mẫu dương. Khi toàn batch không có anchor hợp lệ, phần loss bằng 0 cần giữ tương thích autograd.

### 4. Chưa tách được tác động của loss và backbone

**Mức độ: cao.** Chưa có baseline CRF cùng backbone cho XLM-R, ELECTRA và BamiBERT; baseline PhoBERT V2 còn thiếu nguồn như mục 1. Một lần chạy không đủ diễn giải chênh lệch nhỏ là hiệu quả của phương pháp. Cần cùng dữ liệu, seed, số bước và ngân sách; đối chiếu CRF, SupCon BIO (alpha=0), H-SupCon giữ O và H-SupCon đầy đủ. Chọn alpha/lambda/tau trên dev, chạy ít nhất năm seed, báo cáo khoảng tin cậy và kiểm định ghép cặp. So sánh hai giai đoạn với tối ưu đồng thời vẫn là hướng thực nghiệm, chưa phải kết quả đã chứng minh.

### 5. BamiBERT chưa thể xếp hạng cùng các hàng còn lại

**Mức độ: cao đối với so sánh mô hình.** Log BamiBERT có 5.162 mẫu và 6.336 thực thể vàng, khác hai log 10.278 mẫu và 20.979 thực thể vàng. Chưa xác định được toàn bộ nguồn chia train/dev/test của run này. F1 98,48% chỉ mô tả run đó, không chứng minh tốt hơn ELECTRA hoặc PhoBERT V2. Cần chạy trên cùng tập test trước khi kết luận thứ hạng.

### 6. Cần bằng chứng trực tiếp cho cơ chế và đóng góp mới

**Mức độ: trung bình.** Việc dùng trọng số dương phân cấp là thiết kế được mô tả rõ; chưa có kết quả chứng minh giảm lỗi ranh giới, cải thiện lớp hiếm hoặc tách cụm biểu diễn. Cần phân tích theo độ dài, lỗi biên/loại/bỏ sót, tỷ lệ anchor hợp lệ và phân bố tương đồng. Vì trọng số được chuẩn hóa theo anchor, alpha chỉ có ý nghĩa tương đối giữa các nhóm dương; nếu anchor chỉ có nhóm dương mềm thì hệ số alpha>0 triệt tiêu trong chuẩn hóa. Không diễn giải alpha=0,3 là lực hút tuyệt đối bằng 30% trong mọi trường hợp. Tính mới cần tiếp tục đối chiếu các phương pháp contrastive NER có quan hệ phân cấp/biên, thay vì khẳng định chưa có công trình tương tự từ một danh sách tham khảo hạn chế.

## Những sửa đổi đã thực hiện

- Bổ sung định nghĩa contrastive loss, anchor, mẫu dương/âm, biểu diễn chuẩn hóa, cosine, nhiệt độ và công thức SupCon theo nhãn BIO; liên kết rõ với H-SupCon.
- Làm rõ mẫu số gồm cả dương/âm, loại self-pair, padding và token đặc biệt; bổ sung quy ước loss=0 khi không có anchor hợp lệ.
- Cho phép alpha từ 0 đến 1 để hai trường hợp ablation có định nghĩa; phân biệt vai trò alpha và lambda, nêu rõ tập cặp trong mini-batch.
- Bổ sung trạng thái bắt đầu/kết thúc vào điểm CRF; bỏ diễn giải CRF tự bảo đảm tính hợp lệ BIO khi chưa có ràng buộc cứng.
- Thay phần mô tả 34.413 câu bị dùng lẫn bằng thống kê trực tiếp: 142.218 train, 10.305 dev, 10.278 test; tổng 162.801 câu và 3.711.201 token. Phân bố B-X là CQ 62.915, ĐT 67.001, VBPL 25.522, NG 35.647, SL 14.722, tổng 205.807.
- Đánh dấu số liệu thiếu log, tách mô tả cấu hình khỏi bằng chứng quét, loại khẳng định chắc chắn về ưu thế joint training và cơ chế biểu diễn.
- Giữ nguyên giá trị kết quả và loại biểu đồ người dùng đã chọn; chú thích trục tung bắt đầu ở 97% để thể hiện phạm vi phóng đại.
- Giữ phần VI đã rút gọn và không khôi phục mục “Tín hiệu thực nghiệm của H-SupCon” đã xóa.

## Đối chiếu số liệu có nguồn

| Log | Test | TP / FP / FN | P / R / F1 (%) tính từ số đếm |
|---|---:|---|---|
| XLM-R/14Oct.log | 10.278 | 20.280 / 437 / 699 | 97,8906 / 96,6681 / 97,2755 |
| PhoBERT-V2/14Oct.log | 10.278 | 20.393 / 279 / 586 | 98,6503 / 97,2067 / 97,9232 |
| BamiBERT/14Oct.log | 5.162 | 6.268 / 126 / 68 | 98,0294 / 98,9268 / 98,4760 |

Nguồn nằm trong `../logs_contrastive/`. Số liệu làm tròn khớp bảng hiện có. [review_audit.json](review_audit.json) lưu đường dẫn, SHA-256 của dữ liệu và log, số đếm và kiểm tra nguồn LaTeX. Việc khớp kích thước/token không thay thế xác nhận phiên bản dữ liệu đã dùng ở từng run.

## Kiểm tra bản thảo

- Đã kiểm tra trùng label, khóa trích dẫn, tham chiếu nội bộ và cặp môi trường LaTeX.
- Biên dịch bằng pdfLaTeX và BibTeX; kiểm tra PDF sáu trang, bảng, công thức, hình và tham chiếu sau lần biên dịch cuối.
- Bản trước khi review được lưu tại `main.before_review.tex` để đối chiếu nội dung.
- Không thay đổi checkpoint, log nguồn, dữ liệu hay tự tạo thêm kết quả thực nghiệm.

## Tài liệu nền đã đối chiếu

- [Khosla và cộng sự, Supervised Contrastive Learning, NeurIPS 2020](https://papers.neurips.cc/paper_files/paper/2020/file/d89a66c7c80a29b1bdbab0f2a1a94af8-Paper.pdf): công thức loss nhiều mẫu dương và đầu chiếu.
- [PAP_NER, PLOS ONE](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0353166): quy mô và cấu trúc nhãn; điểm benchmark chỉ dùng tham khảo khi giao thức chưa được xác nhận.
- [seqeval](https://github.com/chakki-works/seqeval): phân biệt evaluator mặc định và chế độ strict/IOB2.
- [SCL-RAI](https://aclanthology.org/2022.coling-1.202/), [CONTaiNER](https://aclanthology.org/2022.acl-long.439/), [BANER](https://aclanthology.org/2025.coling-main.691/): phạm vi tác vụ của các công trình liên quan.
- [BamiBERT](https://arxiv.org/abs/2607.02259): định danh công trình mô hình nền, không xác nhận cấu hình run cục bộ.
