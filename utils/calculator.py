import pandas as pd

DAILY_RATE = {
    '北京': 450,
    '上海': 450,
    '广州': 380,
    '深圳': 380,
    '其他区域': 330,
}
def get_return_date(row):
    """Get the latest valid arrival date as return date."""
    dates = []
    for col in ['第一目的地到达日期', '第二目的地到达日期', '第三目的地到达日期']:
        d = row.get(col)
        if pd.notna(d):
            try:
                d = pd.to_datetime(d).date()
                dates.append(d)
            except Exception:
                continue
    return max(dates) if dates else row['出发日期']

def process_files(company_file_path, client_file_path):
    df_comp = pd.read_excel(company_file_path)
    required_cols_comp = ['申请人', '金额', '出发日期', '单据编号']
    for col in required_cols_comp:
        if col not in df_comp.columns:
            raise ValueError(f"Company reimbursement file missing required column: {col}")

    date_cols = ['出发日期', '第一目的地到达日期', '第二目的地到达日期', '第三目的地到达日期']
    for col in date_cols:
        if col in df_comp.columns:
            df_comp[col] = pd.to_datetime(df_comp[col], errors='coerce').dt.date
        else:
            df_comp[col] = None

    df_comp['返程日期'] = df_comp.apply(get_return_date, axis=1)
    df_comp['公司差旅天数'] = (pd.to_datetime(df_comp['返程日期']) - pd.to_datetime(df_comp['出发日期'])).dt.days + 1

    company_grouped = df_comp.groupby(['申请人', '出发日期', '返程日期']).agg({
        '金额': 'sum',
        '公司差旅天数': 'first',
        '单据编号': lambda x: ','.join(
            pd.Series(x).dropna().astype(str).unique()
        )
    }).reset_index()

    df_client = pd.read_excel(client_file_path)
    required_cols_client = [
        '候选人', '常驻地', '派驻地',
        '结算入场时间', '结算离场时间',
        '差旅人天', '派驻应用', '差旅结算（含税）金额'
    ]
    for col in required_cols_client:
        if col not in df_client.columns:
            raise ValueError(f"Client settlement file missing required column: {col}")

    df_client['候选人'] = df_client['候选人'].astype(str).str.strip()
    df_client['常驻地'] = df_client['常驻地'].astype(str).str.strip()
    df_client['派驻地'] = df_client['派驻地'].astype(str).str.strip()
    df_client['结算入场时间'] = pd.to_datetime(df_client['结算入场时间'], errors='coerce').dt.date
    df_client['结算离场时间'] = pd.to_datetime(df_client['结算离场时间'], errors='coerce').dt.date
    df_client['差旅人天'] = pd.to_numeric(df_client['差旅人天'], errors='coerce').fillna(0)
    df_client['差旅结算（含税）金额'] = pd.to_numeric(df_client['差旅结算（含税）金额'], errors='coerce').fillna(0)

    df_client = df_client.sort_values(['候选人', '派驻应用', '结算入场时间', '结算离场时间'])
    merged_rows = []
    current = None

    for _, row in df_client.iterrows():
        if current is None:
            current = row.to_dict()
            continue

        same_person = row['候选人'] == current['候选人']
        same_app = row['派驻应用'] == current['派驻应用']
        prev_end = current.get('结算离场时间')
        curr_start = row['结算入场时间']

        # 判断时间是否连续：后一条的入场时间 = 前一条的离场时间 + 1 天
        is_continuous = (
            pd.notna(prev_end)
            and pd.notna(curr_start)
            and (curr_start - prev_end).days == 1
        )

        if same_person and same_app and is_continuous:
            # 合并到当前段：扩展离场时间，累加人天和差旅结算金额
            current['结算离场时间'] = row['结算离场时间']
            current['差旅人天'] = current.get('差旅人天', 0) + row['差旅人天']
            current['差旅结算（含税）金额'] = current.get('差旅结算（含税）金额', 0) + row['差旅结算（含税）金额']
        else:
            merged_rows.append(current)
            current = row.to_dict()

    if current is not None:
        merged_rows.append(current)

    df_client = pd.DataFrame(merged_rows)

    results = []
    for _, emp in company_grouped.iterrows():
        name = emp['申请人']
        comp_start = emp['出发日期']
        comp_end = emp['返程日期']
        comp_days = emp['公司差旅天数']
        comp_total = emp['金额']

        if comp_days <= 0:
            continue

        client_match = df_client[df_client['候选人'] == str(name)]
        if client_match.empty:
            continue

        for _, c in client_match.iterrows():
            if c['常驻地'] == c['派驻地']:
                continue

            cli_start = c['结算入场时间']
            cli_end = c['结算离场时间']
            cli_days = c['差旅人天']

            if pd.isna(cli_start) or pd.isna(cli_end):
                continue

            if comp_start <= cli_start and comp_end >= cli_end:
                city = c['派驻地']
                rate = DAILY_RATE.get(city, DAILY_RATE["其他区域"])

                client_total = rate * cli_days

                daily_rate_comp = comp_total / comp_days

                start_diff = (cli_start - comp_start).days
                end_diff = (comp_end - cli_end).days
                if start_diff in (0, 1) and end_diff in (0, 1):
                    comp_amount_for_cli_days = comp_total
                    subsidy = client_total - comp_total
                else:
                    comp_amount_for_cli_days = daily_rate_comp * cli_days
                    subsidy = client_total - comp_amount_for_cli_days

                subsidy = max(0, round(subsidy, 2))

                results.append({
                    "申请人": name,
                    "单据编号": emp.get('单据编号', ''),
                    "常驻地": c['常驻地'],
                    "派驻地": c['派驻地'],
                    "派驻应用": c['派驻应用'],
                    "公司出发日期": comp_start,
                    "公司返程日期": comp_end,
                    "公司差旅天数": int(comp_days),
                    "公司报销总金额": round(comp_total, 2),
                    "客户结算入场时间": cli_start,
                    "客户结算离场时间": cli_end,
                    "客户差旅人天": int(cli_days),
                    "客户日均标准": rate,
                    "客户包干总额": round(client_total, 2),
                    "公司日均差旅费": round(daily_rate_comp, 2),
                    "公司标准下客户天数总额": round(comp_amount_for_cli_days, 2),
                    "津贴金额": subsidy
                })

    if not results:
        raise ValueError("No subsidy records were generated.")

    df_result = pd.DataFrame(results)

    amount_cols = [
        '公司报销总金额',
        '客户日均标准',
        '客户包干总额',
        '公司日均差旅费',
        '公司标准下客户天数总额',
        '津贴金额',
    ]
    for col in amount_cols:
        if col in df_result.columns:
            df_result[col] = pd.to_numeric(df_result[col], errors='coerce').fillna(0).round(2)

    df_result['备注'] = ''
    if '津贴金额' in df_result.columns:
        df_result.loc[df_result['津贴金额'] == 0, '备注'] = 'Company reimbursement standard is greater than or equal to client standard, subsidy is 0'

    return df_result