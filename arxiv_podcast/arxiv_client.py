import arxiv

def fetch_arxiv_papers(query, max_results=5, categories=None, sort_by=None, sort_order=None, client=None):
    """
    获取 arXiv 论文数据
    
    Args:
        query (str): 搜索查询
        max_results (int): 最大结果数量
        categories (list): 论文分类列表
        sort_by (str): 排序标准
        sort_order (str): 排序顺序
        client (arxiv.Client, optional): 用于测试的客户端对象
    
    Returns:
        list: 论文数据列表
    """
    if categories:
        cat_query = ' OR '.join(f'cat:{c}' for c in categories)
        full_query = f"{query} AND ({cat_query})"
    else:
        full_query = query
        
    # 修正：将字符串映射为枚举类型（兼容 config.yaml 中的字符串配置）
    sort_by_map = {
        "relevance": arxiv.SortCriterion.Relevance,
        "lastUpdatedDate": arxiv.SortCriterion.LastUpdatedDate,
        "submittedDate": arxiv.SortCriterion.SubmittedDate,
    }
    sort_order_map = {
        "ascending": arxiv.SortOrder.Ascending,
        "descending": arxiv.SortOrder.Descending,
    }
    
    sort_by_enum = sort_by_map.get(sort_by, arxiv.SortCriterion.SubmittedDate)
    sort_order_enum = sort_order_map.get(sort_order, arxiv.SortOrder.Descending)
    
    # 使用提供的客户端或创建新客户端
    client = client or arxiv.Client()
    
    search = arxiv.Search(
        query=full_query,
        max_results=max_results,
        sort_by=sort_by_enum,
        sort_order=sort_order_enum
    )
    
    results = []
    for result in client.results(search):
        results.append({
            "title": result.title,
            "summary": result.summary,
            "published": result.published.strftime('%Y-%m-%d'),
            "authors": [a.name for a in result.authors],
            "pdf_url": result.pdf_url,
            "arxiv_id": result.entry_id.split('/')[-1]
        })
    
    return results