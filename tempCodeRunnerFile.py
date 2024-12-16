def group_texts_by_index(texts, found_keywords):
    grouped_texts = []
    
    # Đảm bảo rằng found_keywords đã được sắp xếp
    found_keywords = sorted(found_keywords)

    # Nhóm các chunk từ chỉ số 0 đến chỉ số đầu tiên trong found_keywords
    if found_keywords[0] > 0:
        grouped_texts.append(list(range(0, found_keywords[0])))  # Các chunk từ 0 đến trước chỉ số đầu tiên trong found_keywords
    
    # Nhóm các chunk giữa các chỉ số liên tiếp trong found_keywords
    for i in range(1, len(found_keywords)):
        if found_keywords[i] > found_keywords[i-1] + 1:  # Nếu có khoảng cách giữa các chỉ số
            grouped_texts.append(list(range(found_keywords[i-1] + 1, found_keywords[i])))  # Các chunk nằm giữa

    # Nhóm phần còn lại sau chỉ số cuối cùng trong found_keywords
    if found_keywords[-1] < len(texts) - 1:
        grouped_texts.append(list(range(found_keywords[-1] + 1, len(texts))))  # Các chunk từ phần tử cuối cùng

    # Thêm các phần tử trong found_keywords vào nhóm riêng
    grouped_texts.extend([[i] for i in found_keywords])

    return grouped_texts